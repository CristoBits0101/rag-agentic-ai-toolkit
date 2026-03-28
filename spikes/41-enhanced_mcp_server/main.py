# --- DEPENDENCIAS ---
import asyncio
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from orchestration.enhanced_mcp_workflow import run_enhanced_mcp_demo


async def _main() -> None:
    result = await run_enhanced_mcp_demo()
    print("=== Directory Count ===")
    print(result["directory_count"])
    print("\n=== File Content ===")
    print(result["file_content"])
    print("\n=== Code Review ===")
    print(result["review_output"])
    print("\n=== Documentation ===")
    print(result["documentation_output"])
    print("\n=== Conversation ===")
    print(result["conversation_output"])
    print("\n=== Generated Documentation ===")
    print(result["generated_text"])


if __name__ == "__main__":
    asyncio.run(_main())
