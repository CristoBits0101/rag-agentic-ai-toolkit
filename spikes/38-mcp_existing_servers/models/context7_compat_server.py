# --- DEPENDENCIAS ---
from fastmcp import FastMCP

from config.mcp_existing_servers_config import LIBRARY_CATALOG

mcp = FastMCP(
    "Context7CompatServer",
    instructions=(
        "This server exposes Context7 style documentation lookup tools. "
        "Use resolve-library-id before query-docs."
    ),
)


def _normalize_library_name(library_name: str) -> str:
    return library_name.strip().lower().replace("_", "-")


@mcp.tool(name="resolve-library-id")
def resolve_library_id(libraryName: str, query: str = "") -> str:
    normalized = _normalize_library_name(libraryName)
    matches: list[str] = []
    for library_id, payload in LIBRARY_CATALOG.items():
        haystack = " ".join([library_id, payload["title"], payload["description"], query]).lower()
        if normalized in haystack:
            matches.append(
                "\n".join(
                    [
                        f"- Title: {payload['title']}",
                        f"  Context7-compatible library ID: {library_id}",
                        f"  Description: {payload['description']}",
                        f"  Code Snippets: {payload['snippets']}",
                        f"  Source Reputation: {payload['source_reputation']}",
                        f"  Benchmark Score: {payload['benchmark_score']}",
                        f"  Trust Score: {payload['trust_score']}",
                    ]
                )
            )
    if not matches:
        return f"No library found for {libraryName}."
    return "\n\n".join(matches)


@mcp.tool(name="query-docs")
def query_docs(libraryId: str, query: str, tokens: int = 5000) -> str:
    payload = LIBRARY_CATALOG.get(libraryId)
    if payload is None:
        return f"Unknown libraryId: {libraryId}"
    text = (
        f"Library: {payload['title']}\n"
        f"Requested query: {query}\n"
        f"Token budget: {tokens}\n\n"
        f"{payload['body']}"
    )
    return text[:tokens]
