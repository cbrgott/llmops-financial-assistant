import asyncio

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


async def main():
    async with streamable_http_client(
        "http://127.0.0.1:8000/mcp"
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