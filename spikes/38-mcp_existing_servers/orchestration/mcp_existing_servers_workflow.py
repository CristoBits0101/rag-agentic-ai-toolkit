# --- DEPENDENCIAS ---
import asyncio
import sys
from contextlib import asynccontextmanager

from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from fastmcp.client.transports import StreamableHttpTransport

from config.mcp_existing_servers_config import HTTP_HOST
from config.mcp_existing_servers_config import HTTP_PORT
from config.mcp_existing_servers_config import REAL_CONTEXT7_NPX_PACKAGE
from config.mcp_existing_servers_config import REAL_CONTEXT7_URL
from config.mcp_existing_servers_config import SPIKE_ROOT
from models.context7_compat_server import mcp


def build_stdio_transport() -> StdioTransport:
    return StdioTransport(
        command=sys.executable,
        args=[str(SPIKE_ROOT / "models" / "context7_stdio_server.py")],
        cwd=str(SPIKE_ROOT),
    )


def build_http_transport(url: str | None = None) -> StreamableHttpTransport:
    return StreamableHttpTransport(url=url or f"http://{HTTP_HOST}:{HTTP_PORT}/mcp")


def describe_real_world_transport_targets() -> dict[str, str]:
    return {
        "stdio_command": f"npx -y {REAL_CONTEXT7_NPX_PACKAGE}",
        "http_url": REAL_CONTEXT7_URL,
    }


async def list_tools_with_transport(transport) -> list[str]:
    async with Client(transport) as client:
        tools = await client.list_tools()
        return [tool.name for tool in tools]


async def resolve_and_query_fastmcp(transport) -> dict[str, str]:
    async with Client(transport) as client:
        tools = await client.list_tools()
        resolved = await client.call_tool(
            "resolve-library-id",
            {
                "libraryName": "fastmcp",
                "query": "I want to create a new MCP server using the fastmcp Python framework",
            },
        )
        docs = await client.call_tool(
            "query-docs",
            {
                "libraryId": "/llmstxt/gofastmcp_llms-full_txt",
                "query": "I want to fetch the code snippets and the documentation",
                "tokens": 1200,
            },
        )
    return {
        "tool_count": str(len(tools)),
        "resolve_text": resolved.content[0].text,
        "docs_text": docs.content[0].text,
    }


@asynccontextmanager
async def local_http_server():
    task = asyncio.create_task(mcp.run_http_async(host=HTTP_HOST, port=HTTP_PORT))
    await asyncio.sleep(0.35)
    try:
        yield f"http://{HTTP_HOST}:{HTTP_PORT}/mcp"
    finally:
        task.cancel()
        try:
            await task
        except BaseException:
            pass


async def run_existing_mcp_servers_demo() -> dict[str, dict[str, str] | list[str] | dict[str, str]]:
    stdio_transport = build_stdio_transport()
    stdio_tools = await list_tools_with_transport(stdio_transport)
    stdio_payload = await resolve_and_query_fastmcp(stdio_transport)
    async with local_http_server() as url:
        http_transport = build_http_transport(url)
        http_tools = await list_tools_with_transport(http_transport)
        http_payload = await resolve_and_query_fastmcp(http_transport)
    return {
        "real_world_targets": describe_real_world_transport_targets(),
        "stdio": {"tools": ", ".join(stdio_tools), **stdio_payload},
        "http": {"tools": ", ".join(http_tools), **http_payload},
    }
