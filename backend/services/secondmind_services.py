from agents.graph_builder import build_graph
from config import DB_URL
from aimodel import embed

from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.store.postgres.aio import AsyncPostgresStore


class SecondMindService:

    def __init__(self):
        self.memory = None
        self.store = None
        self.chatbot = None

        self.memory_cm = None
        self.store_cm = None

    async def initialize(self):

        self.memory_cm = AsyncPostgresSaver.from_conn_string(
            DB_URL
        )

        self.memory = await self.memory_cm.__aenter__()

        self.store_cm = AsyncPostgresStore.from_conn_string(
            DB_URL,
            index={
                "dims": 768,
                "embed": embed
            }
        )

        self.store = await self.store_cm.__aenter__()

        await self.store.setup()
        await self.memory.setup()

        self.chatbot = await build_graph(
            self.memory,
            self.store
        )

    async def cleanup(self):

        if self.memory_cm:
            await self.memory_cm.__aexit__(
                None, None, None
            )

        if self.store_cm:
            await self.store_cm.__aexit__(
                None, None, None
            )

    async def chat(self, query, config):

        result = await self.chatbot.ainvoke(
            {
                "messages": query
            },
            config=config
        )

        return result


secondmind = SecondMindService()