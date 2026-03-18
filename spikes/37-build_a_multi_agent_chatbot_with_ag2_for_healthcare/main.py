# --- DEPENDENCIAS ---
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from orchestration.healthcare_chatbot_workflow import run_healthcare_demo


if __name__ == "__main__":
    run_healthcare_demo()