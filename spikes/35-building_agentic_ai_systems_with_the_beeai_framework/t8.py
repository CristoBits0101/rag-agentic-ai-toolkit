# --- DEPENDENCIAS ---
import asyncio
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from orchestration.beeai_tutorial_workflow import controlled_execution_example


if __name__ == "__main__":
    print(asyncio.run(controlled_execution_example()).answer.text)