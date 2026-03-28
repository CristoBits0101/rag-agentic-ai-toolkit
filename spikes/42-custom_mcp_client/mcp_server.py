# --- DEPENDENCIAS ---
import logging
from pathlib import Path

from fastmcp import FastMCP

logging.getLogger("fastmcp").setLevel(logging.WARNING)

mcp = FastMCP("lab-server")
BASE_DIR = Path(__file__).resolve().parent


@mcp.tool()
def echo(text: str) -> str:
    return f"Echo: {text}"


@mcp.tool()
def write_file(path: str, content: str) -> str:
    file_path = BASE_DIR / path
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content, encoding="utf-8")
    return f"Successfully wrote to {path}"


@mcp.resource("file://resources/{filename}")
def read_resource_file(filename: str) -> str:
    file_path = BASE_DIR / "resources" / filename
    if not file_path.exists():
        return f"File not found: {filename}"
    return file_path.read_text(encoding="utf-8")


@mcp.prompt()
def review_file(filename: str) -> str:
    return (
        f"Please review the file '{filename}' and provide:\n\n"
        "1. A summary of its contents\n"
        "2. Key points or sections\n"
        "3. Any suggestions for improvement\n"
        "4. Overall quality assessment\n\n"
        "Use the appropriate tools to read the file if needed."
    )


if __name__ == "__main__":
    mcp.run()
