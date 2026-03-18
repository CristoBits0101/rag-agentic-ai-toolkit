# --- DEPENDENCIAS ---
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from orchestration.ag2_tutorial_workflow import run_ag2_tutorial_demo


if __name__ == "__main__":
    run_ag2_tutorial_demo()