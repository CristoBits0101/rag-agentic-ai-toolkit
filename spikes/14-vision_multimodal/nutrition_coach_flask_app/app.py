# --- DEPENDENCIAS ---
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from orchestration.nutrition_coach_app_orchestration import create_nutrition_coach_app
from orchestration.nutrition_coach_app_orchestration import launch_nutrition_coach_app

app = create_nutrition_coach_app()


if __name__ == "__main__":
    launch_nutrition_coach_app()
