# --- DEPENDENCIAS ---
from pathlib import Path

SPIKE_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_DIR = SPIKE_ROOT / "workspace"
HTTP_HOST = "127.0.0.1"
HTTP_PORT = 8000
HTTP_PATH = "/mcp"
GUI_PORT = 7865
HOST_PORT = 7866
SERVER_NAME = "Advanced HTTP File Server"
CLIENT_NAME = "Advanced HTTP Client"
HOST_NAME = "Advanced HTTP Host"

SAMPLE_FILES = {
    "README.md": "# README\nWelcome to the MCP workspace!\n",
    "test.txt": "# Test File\nThis is a test file in the workspace.\n",
    "example.py": "def add(a: int, b: int) -> int:\n    return a + b\n",
}

SAMPLE_CODE = "def add(a, b):\n    return a + b\n"