# --- DEPENDENCIAS ---
import asyncio
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from orchestration.advanced_http_workflow import run_advanced_http_demo


async def _main() -> None:
    result = await run_advanced_http_demo()
    print("=== Tools ===")
    print(result["tool_names"])
    print("\n=== Declared Roots ===")
    print(result["declared_roots"])
    print("\n=== Roots Tool ===")
    print(result["roots_text"])
    print("\n=== List Files ===")
    print(result["list_text"])
    print("\n=== Write File ===")
    print(result["write_text"])
    print("\n=== Resource ===")
    print(result["resource_text"])
    print("\n=== Prompt ===")
    print(result["prompt_text"])
    print("\n=== Sampling ===")
    print(result["sampling_text"])
    print("\n=== Host Write ===")
    print(result["host_write_text"])
    print("\n=== Host Roots ===")
    print(result["host_roots_text"])


if __name__ == "__main__":
    asyncio.run(_main())