# --- DEPENDENCIAS ---
import asyncio
import socket
from contextlib import asynccontextmanager

from config.advanced_mcp_http_config import HTTP_HOST
from config.advanced_mcp_http_config import SAMPLE_CODE
from config.advanced_mcp_http_config import WORKSPACE_DIR
from models.advanced_http_client_base import MCPHTTPClient
from models.advanced_http_host_app import MCPHTTPHostApp
from models.advanced_http_mcp_server import mcp
from models.advanced_http_mcp_server import ensure_workspace_files


def _get_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((HTTP_HOST, 0))
        return sock.getsockname()[1]


@asynccontextmanager
async def local_http_server():
    port = _get_free_port()
    task = asyncio.create_task(mcp.run_http_async(host=HTTP_HOST, port=port, path="/mcp"))
    await asyncio.sleep(0.35)
    try:
        yield f"http://{HTTP_HOST}:{port}"
    finally:
        task.cancel()
        try:
            await task
        except BaseException:
            pass


def _text_from_tool_result(result) -> str:
    return "\n".join(content.text for content in result.content if hasattr(content, "text"))


async def run_advanced_http_demo() -> dict[str, object]:
    ensure_workspace_files()
    async with local_http_server() as server_url:
        base_client = MCPHTTPClient(server_url, WORKSPACE_DIR)
        host_app = MCPHTTPHostApp(server_url, str(WORKSPACE_DIR))
        try:
            tool_names = [tool.name for tool in await base_client.list_tools()]
            roots_result = await base_client.call_tool("list_roots_boundary", {})
            roots_text = _text_from_tool_result(roots_result)
            list_result = await base_client.call_tool("list_files", {"directory": "."})
            list_text = _text_from_tool_result(list_result)
            write_result = await base_client.call_tool(
                "write_file",
                {"filepath": "notes/hello.txt", "content": "Hello from HTTP MCP!"},
            )
            write_text = _text_from_tool_result(write_result)
            resource_contents = await base_client.read_resource("file://workspace/test.txt")
            resource_text = "\n".join(content.text for content in resource_contents if hasattr(content, "text"))
            prompt_result = await base_client.get_prompt("review_code", {"filename": "example.py"})
            prompt_text = "\n".join(
                message.content.text for message in prompt_result.messages if hasattr(message.content, "text")
            )
            sampling_result = await base_client.call_tool(
                "analyze_code",
                {"code": SAMPLE_CODE, "focus": "security"},
            )
            sampling_text = _text_from_tool_result(sampling_result)
            host_write_text = await host_app.ask("Create a file called hello.txt with the message: Hello from HTTP MCP!")
            host_roots_text = await host_app.ask("What roots are available?")
        finally:
            await host_app.cleanup()
            await base_client.cleanup()

    return {
        "tool_names": tool_names,
        "roots_text": roots_text,
        "list_text": list_text,
        "write_text": write_text,
        "resource_text": resource_text,
        "prompt_text": prompt_text,
        "sampling_text": sampling_text,
        "sampling_requests": list(base_client.sampling_requests),
        "host_write_text": host_write_text,
        "host_roots_text": host_roots_text,
        "declared_roots": base_client.describe_roots(),
    }