# --- DEPENDENCIAS ---
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
ASSETS_DIR = BASE_DIR / "assets"
OLLAMA_VISION_API_URL = "http://127.0.0.1:11434/api/chat"
LLAVA_MODEL_NAME = "llava"
LLAMA32_VISION_MODEL_NAME = "llama3.2-vision"
QWEN25_VL_MODEL_NAME = "qwen2.5vl:3b"
REAL_CITY_SCENE_IMAGE_PATH = ASSETS_DIR / "city_scene_real.png"
REAL_NUTRITION_LABEL_IMAGE_PATH = ASSETS_DIR / "nutrition_label_real.png"
REAL_CITY_SCENE_QUERY = "Describe this image and count how many cars you can see."
REAL_NUTRITION_QUERY = "Read the visible nutrition label text and tell me the sodium value."
