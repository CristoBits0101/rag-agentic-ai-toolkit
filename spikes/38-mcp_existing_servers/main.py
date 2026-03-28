# --- DEPENDENCIAS ---
import asyncio
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from orchestration.mcp_existing_servers_workflow import run_existing_mcp_servers_demo


async def _main() -> None:
    result = await run_existing_mcp_servers_demo()
    print("=== Real Context7 Targets ===")
    print(result["real_world_targets"])
    print("\n=== STDIO Demo ===")
    print(result["stdio"]["tools"])
    print(result["stdio"]["resolve_text"])
    print(result["stdio"]["docs_text"][:700])
    print("\n=== HTTP Demo ===")
    print(result["http"]["tools"])
    print(result["http"]["resolve_text"])
    print(result["http"]["docs_text"][:700])


if __name__ == "__main__":
    asyncio.run(_main())
