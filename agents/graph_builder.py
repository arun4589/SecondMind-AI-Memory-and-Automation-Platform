from langgraph.graph import StateGraph, START,END
from langgraph.prebuilt import ToolNode, tools_condition
from schema import ChatbotState
from agents.nodes import get_chat_node,summerisation_node, remember_node
from mcps.clients import load_tools
from aimodel import llm


async def build_graph(memory,store):

    tools = await load_tools()
    print('_'*50)
    for tool in tools:
        print(tool.name)
    print('-'*50)    
    llm_with_tools = llm.bind_tools(tools)

    graph = StateGraph(ChatbotState)
    graph.add_node('remember',remember_node)
    graph.add_node(
        "chat_node",
        get_chat_node(llm_with_tools)
    )

    graph.add_node(
        "tools",
        ToolNode(tools)
    )
    graph.add_node(
        "chat_summary",
        summerisation_node()
    )

    graph.add_edge(START, "remember")
    graph.add_edge("remember","chat_node")
    graph.add_conditional_edges(
        "chat_node",
        tools_condition
    )
    graph.add_edge(
        "tools",
        "chat_node"
    )
    graph.add_edge("chat_node","chat_summary")
    graph.add_edge("chat_summary",END)

    return graph.compile(
        checkpointer=memory,
        store=store
    )