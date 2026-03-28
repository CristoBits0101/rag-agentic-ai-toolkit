# --- DEPENDENCIAS ---
from fastmcp import FastMCP

from config.mcp_application_config import MET_OBJECTS

mcp = FastMCP("MetMuseumServer", instructions="Search artworks and retrieve object details from a local Met Museum sample catalog.")


@mcp.tool(name="search-met-art")
def search_met_art(query: str) -> str:
    lowered = query.lower()
    matches = [
        item for item in MET_OBJECTS if lowered in item["title"].lower() or lowered in item["artist"].lower() or lowered in item["department"].lower()
    ]
    if not matches:
        matches = MET_OBJECTS[:1]
    lines = [f"- {item['objectID']}: {item['title']} by {item['artist']}" for item in matches]
    return "\n".join(lines)


@mcp.tool(name="get-artwork-details")
def get_artwork_details(object_id: int) -> str:
    for item in MET_OBJECTS:
        if item["objectID"] == object_id:
            return (
                f"Title: {item['title']}\n"
                f"Artist: {item['artist']}\n"
                f"Department: {item['department']}\n"
                f"Summary: {item['summary']}"
            )
    return f"Object {object_id} was not found."
