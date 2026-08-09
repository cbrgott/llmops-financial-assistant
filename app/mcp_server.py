from mcp.server import MCPServer

from app.tools import financial_search


mcp = MCPServer(
    name="financial-assistant-tools"
)


@mcp.tool()
def search_financial_documents(query: str) -> str:
    """
    Search Tongaat Hulett's indexed financial and ESG documents.
    """
    return financial_search(query)


if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=8000
    )