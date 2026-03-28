# --- DEPENDENCIAS ---
import asyncio
import sys
from contextlib import asynccontextmanager

from langchain_mcp_adapters.client import MultiServerMCPClient

from config.mcp_application_config import HTTP_HOST
from config.mcp_application_config import HTTP_PORT
from config.mcp_application_config import SPIKE_ROOT
from models.context7_http_server import mcp as context7_http_server
from models.mcp_application_agent import SessionPersistentMcpAgent


@asynccontextmanager
async def local_context7_http_server():
    task = asyncio.create_task(context7_http_server.run_http_async(host=HTTP_HOST, port=HTTP_PORT))
    await asyncio.sleep(0.35)
    try:
        yield f"http://{HTTP_HOST}:{HTTP_PORT}/mcp"
    finally:
        task.cancel()
        try:
            await task
        except BaseException:
            pass


@asynccontextmanager
async def build_application_agent():
    async with local_context7_http_server() as url:
        client = MultiServerMCPClient(
            {
                "context7": {
                    "url": url,
                    "transport": "streamable_http",
                },
                "met-museum": {
                    "command": sys.executable,
                    "args": [str(SPIKE_ROOT / "models" / "met_museum_stdio_server.py")],
                    "cwd": str(SPIKE_ROOT),
                    "transport": "stdio",
                },
            }
        )
        tools = await client.get_tools()
        yield SessionPersistentMcpAgent(tools)


async def run_mcp_application_demo() -> dict[str, str]:
    async with build_application_agent() as agent:
        intro = agent.introduce()
        docs_answer = await agent.ask("How do I create an MCP server with FastMCP?")
        museum_answer = await agent.ask("Show me a Met Museum artwork by Van Gogh.")
        memory_answer = await agent.ask("What do you remember from this session?")
    return {
        "intro": intro,
        "docs_answer": docs_answer,
        "museum_answer": museum_answer,
        "memory_answer": memory_answer,
    }
