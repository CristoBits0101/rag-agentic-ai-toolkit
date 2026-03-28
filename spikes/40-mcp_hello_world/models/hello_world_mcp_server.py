# --- DEPENDENCIAS ---
from pathlib import Path

from fastmcp import FastMCP

from config.hello_mcp_config import DOCUMENT_DIRECTORY

mcp = FastMCP(
    name="CalculatorMCPServer",
    instructions="This server provides data analysis tools. Call add and subtract and use resources and prompts for review.",
)


@mcp.tool()
def add(a: int, b: int) -> int:
    return a + b


@mcp.tool()
def subtract(a: int, b: int) -> int:
    return a - b


@mcp.resource("file:///endpoint/{name}")
def return_template_document(name: str) -> str:
    return f"Document contents of {name}"


@mcp.resource("file://endpoint2/{name}")
def read_document(name: str) -> str:
    path = DOCUMENT_DIRECTORY / name
    if not path.exists():
        return f"Document '{name}' not found in path directory"
    return path.read_text(encoding="utf-8")


@mcp.prompt(title="Code Review")
def review_code(code: str) -> str:
    return f"Please review this code:\n\n{code}"
