# --- DEPENDENCIAS ---
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from config.nutrition_coach_config import NUTRITION_COACH_SUPPORTED_MODELS
from orchestration.nutrition_coach_lab_runner import run_nutrition_coach_lab


if __name__ == "__main__":
    run_nutrition_coach_lab(NUTRITION_COACH_SUPPORTED_MODELS[0])
