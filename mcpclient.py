import requests
import json


# MCP server base URL
BASE_URL = "http://0.0.0.0:8000/sse"


from mcp import ClientSession, StdioServerParameters, types

from mcp.client.sse import sse_client


async def run():
    async with sse_client(url=BASE_URL) as streams:
        async with ClientSession(streams[0], streams[1]) as session:
            await session.initialize()
            tools=await session.list_tools()
            print("Available tools:", tools)
            result=await session.read_resource("greeting://World")
            print("Result:", result)
        

if __name__ == "__main__":
    import asyncio

    asyncio.run(run())