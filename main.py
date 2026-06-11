import asyncio
from agents.graph_builder import build_graph
from config import CONFIG,DB_URL
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.store.postgres.aio import AsyncPostgresStore
from aimodel import embed
import sys

if sys.platform == "win32":
    asyncio.set_event_loop_policy(
        asyncio.WindowsSelectorEventLoopPolicy()
    )

async def main():

    async with AsyncPostgresSaver.from_conn_string(
        DB_URL
    ) as memory:
        async with AsyncPostgresStore.from_conn_string(DB_URL,index={ "dims": 768, "embed": embed,}) as store:
            await store.setup()
            await memory.setup()
            chatbot = await build_graph(memory,store)

            while True:

                query = input("\nYou : ")

                if query.lower() in ["exit", "quit"]:
                    break

                result = await chatbot.ainvoke(
                {
                    "messages": [
                        HumanMessage(content=query)
                    ]
                },
                config=CONFIG
                )

                print(
                "\nAssistant :",
                result["messages"][-1].content,
                "\n",
                "*"*50
                )
                print(result["messages"])
            

if __name__ == "__main__":
    asyncio.run(main())


