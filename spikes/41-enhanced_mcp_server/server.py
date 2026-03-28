# --- DEPENDENCIAS ---
from datetime import datetime
from pathlib import Path
import asyncio

from fastmcp import Context
from fastmcp import FastMCP
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent


class DocumentGeneratorSchema(BaseModel):
    file_path: str
    name: str


mcp = FastMCP("File Operations MCP Server")


def get_path(relative_path: str) -> Path:
    path = (BASE_DIR / relative_path).resolve()
    path.relative_to(BASE_DIR)
    return path


@mcp.tool()
async def write_file(file_path: str, content: str, ctx: Context) -> str:
    path = get_path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    total = max(len(content), 1)
    chunk_size = max(total // 10, 1)
    written = 0
    with open(path, "w", encoding="utf-8") as handle:
        for index in range(0, len(content), chunk_size):
            handle.write(content[index:index + chunk_size])
            written = min(index + chunk_size, len(content))
            await ctx.report_progress(progress=written, total=len(content), message=f"Writing progress: {written}/{len(content)}")
            await asyncio.sleep(0.01)
    await ctx.report_progress(progress=total, total=total, message="Write complete")
    await ctx.info(f"File written successfully to: {file_path}")
    return f"File written successfully to: {file_path}"


@mcp.tool()
async def delete_file(file_path: str, ctx: Context) -> str:
    path = get_path(file_path)
    if path.is_file():
        path.unlink()
        await ctx.info(f"Successfully deleted file {file_path}")
        return f"Successfully deleted file {file_path}"
    if path.is_dir():
        await ctx.warning(f"Error: {file_path} is a directory, not a file")
        return f"Error: {file_path} is a directory, not a file"
    await ctx.warning(f"File not found: {file_path}")
    return f"File not found: {file_path}"


@mcp.resource("file:///{file_name}")
async def read_file_resource(file_name: str) -> dict:
    try:
        path = get_path(file_name)
    except ValueError as exc:
        return {"error": f"Error reading file: {exc}"}
    if not path.exists() or not path.is_file():
        return {"error": f"Error: {file_name} is not a valid file"}
    return {"file_content": path.read_text(encoding="utf-8")}


@mcp.resource("dir://.")
async def list_files_resource() -> dict:
    path = get_path(".")
    items = []
    for item in path.iterdir():
        stat = item.stat()
        items.append(
            {
                "name": item.name,
                "path": str(item.relative_to(BASE_DIR)),
                "type": "directory" if item.is_dir() else "file",
                "size": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            }
        )
    return {"items": sorted(items, key=lambda item: (item["type"], item["name"]))}


@mcp.prompt()
async def code_review(file_path: str, ctx: Context) -> str:
    path = get_path(file_path)
    if not path.exists() or not path.is_file():
        error_msg = f"Error: {file_path} is not a valid file"
        await ctx.warning(error_msg)
        raise FileNotFoundError(error_msg)
    current_code = path.read_text(encoding="utf-8").strip()
    language = path.suffix.lower()
    prompt = (
        "You are an expert code editor. Review the following code quality.\n\n"
        f"File: {file_path}\n"
        f"Language (file suffix): {language or 'unknown'}\n\n"
        "Current code:\n'''\n"
        f"{current_code}\n"
        "'''\n\n"
        "Provide a comprehensive evaluation of the code:"
    )
    await ctx.info("Successfully returned prompt")
    return prompt


@mcp.prompt()
async def documentation_generator(ctx: Context) -> str:
    result = await ctx.elicit(
        message="Please provide the subject file name and the documentation file name",
        response_type=DocumentGeneratorSchema,
    )
    file_path = result.data.file_path
    path = get_path(file_path)
    if not path.exists() or not path.is_file():
        error_msg = f"Error: {file_path} is not a valid file"
        await ctx.warning(error_msg)
        raise FileNotFoundError(error_msg)
    code = path.read_text(encoding="utf-8").strip()
    language = path.suffix.lower()
    doc_name = result.data.name
    prompt = (
        "You are an expert technical writer and documentation specialist. Create documentation for the following code file:\n\n"
        f"File: {file_path}\n"
        f"Language (file suffix): {language or 'unknown'}\n\n"
        "Current code:\n'''\n"
        f"{code}\n"
        "'''\n\n"
        "Use MCP tools available to you to create the separate documentation file:\n"
        f"- **CRITICAL DETAIL: Name that separate document EXACTLY: {doc_name}**\n"
        "- Add the .md suffix yourself if the name doesn't include it already"
    )
    await ctx.info("Successfully returned prompt")
    return prompt


if __name__ == "__main__":
    print("Starting File Operations Server...")
    mcp.run()
