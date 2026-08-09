from mcp.server import MCPServer
from mcp.server.transport_security import TransportSecuritySettings

from app.tools import financial_search


mcp = MCPServer(
    name="financial-assistant-tools",
    transport_security=TransportSecuritySettings(
        enable_dns_rebinding_protection=True,
        allowed_hosts=[
            "financial-assistant-mcp.livelystone-9aa70074.eastus.azurecontainerapps.io"
        ],
    ),
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
        port=8000,
    )