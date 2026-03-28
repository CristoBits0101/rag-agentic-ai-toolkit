# --- DEPENDENCIAS ---
import asyncio
import json
import socket
import sys
from contextlib import asynccontextmanager

from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from fastmcp.client.transports import StreamableHttpTransport
from langchain_mcp_adapters.client import MultiServerMCPClient

from config.hello_mcp_config import DOCUMENT_DIRECTORY
from config.hello_mcp_config import EXAMPLE_FILES
from config.hello_mcp_config import SPIKE_ROOT
from models.hello_world_mcp_server import mcp


def ensure_documents_exist() -> None:
    DOCUMENT_DIRECTORY.mkdir(parents=True, exist_ok=True)
    for file_name, content in EXAMPLE_FILES.items():
        path = DOCUMENT_DIRECTORY / file_name
        if not path.exists():
            path.write_text(content, encoding="utf-8")


async def call_add_tool_in_memory(a: int, b: int):
    async with Client(mcp) as client:
        return await client.call_tool("add", {"a": a, "b": b})


async def list_tools_in_memory() -> list[str]:
    async with Client(mcp) as client:
        tools = await client.list_tools()
        return [tool.name for tool in tools]


async def read_template_resource(name: str) -> str:
    async with Client(mcp) as client:
        result = await client.read_resource(f"file:///endpoint/{name}")
        return result[0].text


async def read_disk_resource(name: str) -> str:
    async with Client(mcp) as client:
        result = await client.read_resource(f"file://endpoint2/{name}")
        return result[0].text


async def get_review_prompt(code: str) -> str:
    async with Client(mcp) as client:
        result = await client.get_prompt("review_code", {"code": code})
        return result.messages[0].content.text


@asynccontextmanager
async def local_http_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        probe.bind(("127.0.0.1", 0))
        port = probe.getsockname()[1]
    task = asyncio.create_task(mcp.run_http_async(host="127.0.0.1", port=port))
    await asyncio.sleep(0.35)
    try:
        yield StreamableHttpTransport(url=f"http://127.0.0.1:{port}/mcp")
    finally:
        task.cancel()
        try:
            await task
        except BaseException:
            pass


async def call_add_tool_http(a: int, b: int):
    async with local_http_server() as transport:
        async with Client(transport) as client:
            return await client.call_tool("add", {"a": a, "b": b})


def build_stdio_transport() -> StdioTransport:
    return StdioTransport(
        command=sys.executable,
        args=[str(SPIKE_ROOT / "models" / "hello_world_stdio_server.py")],
        cwd=str(SPIKE_ROOT),
    )


async def call_add_tool_stdio(a: int, b: int):
    async with Client(build_stdio_transport()) as client:
        return await client.call_tool("add", {"a": a, "b": b})


async def run_multi_server_demo() -> dict[str, object]:
    async with local_http_server() as transport:
        client = MultiServerMCPClient(
            {
                "stdio-client": {
                    "command": sys.executable,
                    "args": [str(SPIKE_ROOT / "models" / "hello_world_stdio_server.py")],
                    "cwd": str(SPIKE_ROOT),
                    "transport": "stdio",
                },
                "http-client": {
                    "url": str(transport.url),
                    "transport": "streamable_http",
                },
            }
        )
        tools = await client.get_tools()
        add_tools = [tool for tool in tools if tool.name == "add"]
        raw_results = [await tool.ainvoke({"a": 8, "b": 7}) for tool in add_tools]
        results = [int(value) if isinstance(value, str) and value.isdigit() else value for value in raw_results]
    transcript = [
        "[HUMAN] whats 8 + 7? use tools",
        "[AI] tool call add",
        f"[TOOL] {results[0] if results else '15'}",
        "[AI] The answer is 15 and I used an MCP tool.",
    ]
    return {
        "tool_names": [tool.name for tool in tools],
        "add_results": results,
        "transcript": transcript,
    }


async def run_hello_world_mcp_demo() -> dict[str, object]:
    ensure_documents_exist()
    in_memory_add = await call_add_tool_in_memory(4, 5)
    http_add = await call_add_tool_http(4, 5)
    stdio_add = await call_add_tool_stdio(4, 5)
    return {
        "tools": await list_tools_in_memory(),
        "in_memory_add": in_memory_add.content[0].text,
        "http_add": http_add.content[0].text,
        "stdio_add": stdio_add.content[0].text,
        "template_resource": await read_template_resource("README.txt"),
        "disk_resource": await read_disk_resource("README.txt"),
        "review_prompt": await get_review_prompt("print('hello world')"),
        "multi_server": await run_multi_server_demo(),
    }
