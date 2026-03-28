# --- DEPENDENCIAS ---
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
EXAMPLES_DIR = BASE_DIR / "assets" / "examples"
DEFAULT_TEXT_MODEL = "qwen2.5:7b"
DEFAULT_VISION_MODEL = "qwen2.5vl:3b"
SUPPORTED_VISION_MODELS = ("qwen2.5vl:3b", "llava", "llama3.2-vision")
VISION_API_URL = "http://127.0.0.1:11434/api/chat"
IMAGE_SIZE = (128, 128)
GRADIO_HOST = "127.0.0.1"
GRADIO_PORT = 7864
DEFAULT_WORKFLOW = "analysis"
DEFAULT_DIETARY_PREFERENCE = "balanced"
SUPPORTED_DIETARY_PREFERENCES = (
    "balanced",
    "vegetarian",
    "vegan",
    "gluten-free",
    "high-protein",
)