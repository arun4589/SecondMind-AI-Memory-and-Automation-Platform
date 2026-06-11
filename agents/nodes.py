from aimodel import llm,memory_extractor,embed
from schema import ChatbotState,MemoryDecision
from langchain_core.messages import HumanMessage,RemoveMessage
from config import NO_OF_MSG_TO_KEEP_IN_CONVO,REQ_NO_OF_MSG_TO_SUMMERIZE,LIMIT
from langchain_core.messages import SystemMessage
from prompts.prompt import SYSTEM_PROMPT,MEMORY_PROMPT,SUMMARY_PROMPT
from langchain_core.runnables import RunnableConfig
from langgraph.store.base import BaseStore
import uuid

def get_chat_node(llm_with_tools):
    async def chat_node(state: ChatbotState,config:RunnableConfig,store:BaseStore):
        user_id = config["configurable"]["user_id"]
        ns = ("user", user_id, "details")
        query = ""
        for msg in reversed(state["messages"]):
            if isinstance(msg, HumanMessage):
                query = msg.content
                break
        items = await store.asearch(ns,query=query,limit=LIMIT)
        user_details = "\n".join(it.value.get("data", "") for it in items) if items else ""
        summary = state.get("summary", "no conversation till now")
        messages = [SystemMessage(
        content=SYSTEM_PROMPT.format(user_details_content=user_details or "(empty)",conversation_summary=summary)
        )]
        messages.extend(state["messages"])

        print("-" * 70)
        print(messages)
        print("-" * 70)

        response = await llm_with_tools.ainvoke(
            messages
        )

        print("\n========== TOOL CALLS ==========")
        print(response.tool_calls)
        print("================================\n")

        return {
            "messages": [response]
            
        }

    return chat_node


def summerisation_node():
    async def summarize(state: ChatbotState):
        if len(state["messages"]) < REQ_NO_OF_MSG_TO_SUMMERIZE:
            return {}
        msgs_to_summarize = state["messages"][
            :-NO_OF_MSG_TO_KEEP_IN_CONVO
        ]
        existing_summary = state.get(
            "summary",
            "No previous summary available."
        )
        prompt = SUMMARY_PROMPT.format(
            existing_summary=existing_summary
        )
        messages_for_summary = (
            msgs_to_summarize
            + [HumanMessage(content=prompt)]
        )
        response = await llm.ainvoke(
            messages_for_summary
        )
        return {
            "summary": response.content,
            "messages": [
                RemoveMessage(id=m.id)
                for m in msgs_to_summarize
            ]
        }

    return summarize    



async def remember_node(state: ChatbotState, config: RunnableConfig, store: BaseStore):
    user_id = config["configurable"]["user_id"]
    ns = ("user", user_id, "details")

    # existing memory (all items under namespace)
    items = await store.asearch(ns)
    existing = "\n".join(it.value.get("data", "") for it in items) if items else "(empty)"

    # latest user message
    last_text = state["messages"][-1].content

    decision: MemoryDecision = await memory_extractor.ainvoke(
        [
            SystemMessage(content=MEMORY_PROMPT.format(user_details_content=existing)),
            {"role": "user", "content": last_text},
        ]
    )

    if decision.should_write:
        for mem in decision.memories:
            if mem.is_new and mem.text.strip():
                await store.aput(ns, str(uuid.uuid4()), {"data": mem.text.strip()})

    return {}