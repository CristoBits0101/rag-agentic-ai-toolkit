# --- DEPENDENCIAS ---
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from config.style_finder_fashion_config import STYLE_FINDER_SUPPORTED_MODELS
from orchestration.style_finder_lab_runner import run_style_finder_fashion_rag_app


if __name__ == "__main__":
    run_style_finder_fashion_rag_app(STYLE_FINDER_SUPPORTED_MODELS[2])
