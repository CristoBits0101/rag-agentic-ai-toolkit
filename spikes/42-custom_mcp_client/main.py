# --- DEPENDENCIAS ---
import asyncio
from pathlib import Path

from mcp_client import MCPClient


async def run_custom_client_demo() -> dict[str, object]:
    base_dir = Path(__file__).resolve().parent
    client = MCPClient()
    try:
        await client.connect(str(base_dir / "mcp_server.py"))
        tools = await client.list_tools()
        resources = await client.list_resources()
        prompts = await client.list_prompts()
        echo_result = await client.call_tool("echo", {"text": "Hello MCP!"})
        write_result = await client.call_tool("write_file", {"path": "test.txt", "content": "Hello from MCP client!"})
        resource_result = await client.read_resource("file://resources/project_info.txt")
        prompt_result = await client.get_prompt("review_file", {"filename": "test.txt"})
        return {
            "tool_names": [tool.name for tool in tools],
            "resource_templates": [getattr(resource, "uriTemplate", "") for resource in resources],
            "prompt_names": [prompt.name for prompt in prompts],
            "echo_text": echo_result.content[0].text,
            "write_text": write_result.content[0].text,
            "resource_text": resource_result.contents[0].text,
            "prompt_text": prompt_result.messages[0].content.text,
        }
    finally:
        await client.cleanup()


async def _main() -> None:
    result = await run_custom_client_demo()
    print("=== Tools ===")
    print(result["tool_names"])
    print("\n=== Resources ===")
    print(result["resource_templates"])
    print("\n=== Prompts ===")
    print(result["prompt_names"])
    print("\n=== Echo ===")
    print(result["echo_text"])
    print("\n=== Write ===")
    print(result["write_text"])
    print("\n=== Resource Read ===")
    print(result["resource_text"])
    print("\n=== Prompt ===")
    print(result["prompt_text"])


if __name__ == "__main__":
    asyncio.run(_main())
