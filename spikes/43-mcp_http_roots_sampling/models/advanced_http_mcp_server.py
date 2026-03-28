# --- DEPENDENCIAS ---
from pathlib import Path
import sys

SPIKE_ROOT = Path(__file__).resolve().parents[1]
if str(SPIKE_ROOT) not in sys.path:
    sys.path.insert(0, str(SPIKE_ROOT))

from fastmcp import Context
from fastmcp import FastMCP

from config.advanced_mcp_http_config import HTTP_HOST
from config.advanced_mcp_http_config import HTTP_PATH
from config.advanced_mcp_http_config import HTTP_PORT
from config.advanced_mcp_http_config import SAMPLE_FILES
from config.advanced_mcp_http_config import SERVER_NAME
from config.advanced_mcp_http_config import WORKSPACE_DIR

mcp = FastMCP(SERVER_NAME)


def ensure_workspace_files() -> None:
    WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)
    for relative_path, content in SAMPLE_FILES.items():
        file_path = WORKSPACE_DIR / relative_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        if not file_path.exists():
            file_path.write_text(content, encoding="utf-8")


def resolve_workspace_path(filepath: str) -> Path:
    candidate = (WORKSPACE_DIR / filepath).resolve()
    candidate.relative_to(WORKSPACE_DIR.resolve())
    return candidate


def format_directory_listing(path: Path) -> str:
    items: list[str] = []
    for item in sorted(path.iterdir()):
        relative = item.relative_to(WORKSPACE_DIR)
        item_type = "DIR" if item.is_dir() else "FILE"
        size = item.stat().st_size if item.is_file() else 0
        items.append(f"{item_type}: {relative} ({size} bytes)")
    return "\n".join(items) if items else "Directory is empty"


@mcp.tool()
async def list_roots_boundary(ctx: Context) -> str:
    roots = await ctx.list_roots()
    if not roots:
        return "No roots declared by client."
    lines = ["Declared client roots:"]
    for root in roots:
        name = root.name or "Unnamed root"
        lines.append(f"- {name}: {root.uri}")
    return "\n".join(lines)


@mcp.tool()
def read_file(filepath: str) -> str:
    ensure_workspace_files()
    try:
        path = resolve_workspace_path(filepath)
    except ValueError:
        return "Error: Access denied - path outside workspace roots"
    if not path.exists() or not path.is_file():
        return f"Error: File not found: {filepath}"
    return path.read_text(encoding="utf-8")


@mcp.tool()
def write_file(filepath: str, content: str) -> str:
    ensure_workspace_files()
    try:
        path = resolve_workspace_path(filepath)
    except ValueError:
        return "Error: Access denied - path outside workspace roots"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return f"Successfully wrote {len(content)} characters to {filepath}"


@mcp.tool()
def list_files(directory: str = ".") -> str:
    ensure_workspace_files()
    try:
        path = resolve_workspace_path(directory)
    except ValueError:
        return "Error: Access denied - path outside workspace roots"
    if not path.exists():
        return f"Error: Directory not found: {directory}"
    if not path.is_dir():
        return f"Error: Not a directory: {directory}"
    return format_directory_listing(path)


@mcp.tool()
async def analyze_code(code: str, focus: str = "quality", ctx: Context | None = None) -> str:
    if ctx is None:
        return "Error: Sampling context unavailable"
    sampled = await ctx.sample(
        [
            f"Analyze this code for {focus}:\n{code}",
            "Return concrete findings and keep the answer concise.",
        ],
        system_prompt="You are a security and code quality reviewer.",
        max_tokens=400,
        model_preferences=["local-deterministic-sampling"],
    )
    sampled_text = sampled.text if hasattr(sampled, "text") else str(sampled)
    return f"Sampling analysis for {focus}:\n{sampled_text}"


@mcp.resource("file://workspace/{filename}")
def get_workspace_file(filename: str) -> str:
    ensure_workspace_files()
    path = resolve_workspace_path(filename)
    if not path.exists() or not path.is_file():
        raise ValueError(f"File not found: {filename}")
    return path.read_text(encoding="utf-8")


@mcp.prompt()
def review_code(filename: str) -> str:
    return (
        f"Please review the code in file '{filename}' and provide a summary.\n"
        "Also include bugs security concerns and maintainability suggestions."
    )


@mcp.prompt()
def analyze_security(filename: str) -> str:
    return (
        f"Perform a security analysis of '{filename}' focusing on validation authorization and data exposure.\n"
        "Provide remediation guidance for each issue you find."
    )


if __name__ == "__main__":
    ensure_workspace_files()
    print(f"Starting HTTP MCP Server on http://{HTTP_HOST}:{HTTP_PORT}")
    print(f"Workspace roots: {WORKSPACE_DIR}")
    mcp.run(transport="http", host=HTTP_HOST, port=HTTP_PORT, path=HTTP_PATH)