import asyncio

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


async def main():
    async with streamable_http_client(
        "https://financial-assistant-mcp.livelystone-9aa70074.eastus.azurecontainerapps.io/mcp"
    ) as (read, write):

        async with ClientSession(read, write) as session:
            await session.initialize()

            result = await session.call_tool(
                "search_financial_documents",
                {
                    "query": "What is the company ESG strategy?"
                }
            )

            print(result)


asyncio.run(main())
