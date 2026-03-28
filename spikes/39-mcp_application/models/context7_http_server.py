# --- DEPENDENCIAS ---
from fastmcp import FastMCP

from config.mcp_application_config import LIBRARY_CATALOG

mcp = FastMCP("Context7DocsServer", instructions="Resolve library identifiers and return documentation snippets.")


@mcp.tool(name="resolve-library-id")
def resolve_library_id(libraryName: str, query: str = "") -> str:
    lowered = libraryName.strip().lower()
    matches: list[str] = []
    for library_id, payload in LIBRARY_CATALOG.items():
        if lowered in f"{library_id} {payload['title']} {query}".lower():
            matches.append(
                f"- Title: {payload['title']}\n"
                f"  Context7-compatible library ID: {library_id}\n"
                f"  Description: {payload['body']}"
            )
    return "\n\n".join(matches) if matches else f"No match for {libraryName}."


@mcp.tool(name="query-docs")
def query_docs(libraryId: str, query: str, tokens: int = 2000) -> str:
    payload = LIBRARY_CATALOG.get(libraryId)
    if payload is None:
        return f"Unknown library ID: {libraryId}"
    text = f"Library: {payload['title']}\nQuery: {query}\n\n{payload['body']}"
    return text[:tokens]
