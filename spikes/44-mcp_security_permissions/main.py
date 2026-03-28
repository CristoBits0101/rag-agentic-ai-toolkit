# --- DEPENDENCIAS ---
import asyncio
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from orchestration.permission_workflow import run_permission_demo


async def _main() -> None:
    result = await run_permission_demo()
    print("=== Read File ===")
    print(result["read_text"])
    print("\n=== Write Request ===")
    print(result["write_request_text"])
    print("\n=== Write Result ===")
    print(result["write_result_text"])
    print("\n=== Delete Result ===")
    print(result["delete_text"])
    print("\n=== Prompt ===")
    print(result["prompt_text"])
    print("\n=== Server Audit ===")
    print(result["server_audit_text"])
    print("\n=== Client Audit ===")
    print(result["client_audit_text"])
    print("\n=== Host Request ===")
    print(result["host_request_text"])
    print("\n=== Host Approval ===")
    print(result["host_approval_text"])
    print("\n=== Host Denial ===")
    print(result["host_denial_text"])


if __name__ == "__main__":
    asyncio.run(_main())