# --- DEPENDENCIAS ---
import asyncio
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from orchestration.mcp_application_workflow import run_mcp_application_demo


async def _main() -> None:
    result = await run_mcp_application_demo()
    print("=== Agent Intro ===")
    print(result["intro"])
    print("\n=== Documentation Query ===")
    print(result["docs_answer"])
    print("\n=== Museum Query ===")
    print(result["museum_answer"])
    print("\n=== Memory Query ===")
    print(result["memory_answer"])


if __name__ == "__main__":
    asyncio.run(_main())
