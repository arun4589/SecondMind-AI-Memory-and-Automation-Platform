import json
from langchain_mcp_adapters.client import MultiServerMCPClient

with open("servers.json") as f:
    SERVERS = json.load(f)

client = MultiServerMCPClient(SERVERS)

async def load_tools():
    return await client.get_tools()