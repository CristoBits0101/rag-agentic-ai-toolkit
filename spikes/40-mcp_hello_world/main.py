# --- DEPENDENCIAS ---
import asyncio
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from orchestration.hello_mcp_workflow import run_hello_world_mcp_demo


async def _main() -> None:
    result = await run_hello_world_mcp_demo()
    print("=== Tools ===")
    print(result["tools"])
    print("\n=== In Memory Add ===")
    print(result["in_memory_add"])
    print("\n=== HTTP Add ===")
    print(result["http_add"])
    print("\n=== STDIO Add ===")
    print(result["stdio_add"])
    print("\n=== Template Resource ===")
    print(result["template_resource"])
    print("\n=== Disk Resource ===")
    print(result["disk_resource"])
    print("\n=== Prompt ===")
    print(result["review_prompt"])
    print("\n=== Multi Server Transcript ===")
    for line in result["multi_server"]["transcript"]:
        print(line)


if __name__ == "__main__":
    asyncio.run(_main())
