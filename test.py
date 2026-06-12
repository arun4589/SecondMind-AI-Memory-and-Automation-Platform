# from langgraph.store.postgres import PostgresStore

# DB_URI = "postgresql://postgres:postgres@localhost:5442/postgres?sslmode=disable"

# with PostgresStore.from_conn_string(DB_URI) as store:
#     ns = ("user", "5", "details")
#     items = store.search(ns)

# for it in items:
#     print(it.value["data"])

import asyncio
from aimodel import llm

async def test():

    async for chunk in llm.astream(
        "Tell me a story"
    ):
        print(chunk.content, end="", flush=True)

asyncio.run(test())