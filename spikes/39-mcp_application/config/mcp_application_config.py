# --- DEPENDENCIAS ---
from pathlib import Path

SPIKE_ROOT = Path(__file__).resolve().parents[1]
HTTP_HOST = "127.0.0.1"
HTTP_PORT = 8939
AGENT_INTRO = (
    "I can help with library documentation through Context7 style tools and "
    "with Met Museum collection questions through museum tools."
)
LIBRARY_CATALOG = {
    "/llmstxt/gofastmcp_llms-full_txt": {
        "title": "FastMCP",
        "body": (
            "FastMCP supports tools resources prompts STDIO servers and streamable HTTP servers. "
            "Create a server with FastMCP and connect with Client transports."
        ),
    },
}
MET_OBJECTS = [
    {
        "objectID": 436535,
        "title": "Wheat Field with Cypresses",
        "artist": "Vincent van Gogh",
        "department": "European Paintings",
        "summary": "An oil painting from 1889 featuring swirling sky forms and cypress trees in Provence.",
    },
    {
        "objectID": 437853,
        "title": "The Great Wave",
        "artist": "Katsushika Hokusai",
        "department": "Asian Art",
        "summary": "A famous woodblock print showing a towering wave and distant Mount Fuji.",
    },
]
