# --- DEPENDENCIAS ---
from pathlib import Path

SPIKE_ROOT = Path(__file__).resolve().parents[1]
PORT = 8940
DOCUMENT_DIRECTORY = SPIKE_ROOT / "data" / "documents"
EXAMPLE_FILES = {
    "README.txt": "Hello World MCP example readme.\nThis file is exposed through an MCP resource.",
    "examples.txt": "Example prompts and notes for the calculator MCP server.",
}
