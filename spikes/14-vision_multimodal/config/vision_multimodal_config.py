# --- DEPENDENCIAS ---
from pathlib import Path

SPIKE_ROOT = Path(__file__).resolve().parents[1]
ASSETS_DIR = SPIKE_ROOT / "assets"
STYLE_FINDER_EXAMPLES_DIR = SPIKE_ROOT / "style_finder_fashion_rag_app" / "examples"

DEFAULT_ASSISTANT_PROMPT = (
    "You are a helpful assistant. "
    "Answer the following user query in 1 or 2 sentences: "
)
CITY_SCENE_URL = str(ASSETS_DIR / "city_scene_real.png")
FASHION_IMAGE_URL = str(STYLE_FINDER_EXAMPLES_DIR / "golden_hour_suit.png")
NUTRITION_LABEL_URL = str(ASSETS_DIR / "nutrition_label_real.png")
CAT_IMAGE_URL = str(STYLE_FINDER_EXAMPLES_DIR / "red_coat_street.png")
DEFAULT_VISION_QUERY = "Describe the photo"
CAR_COUNT_QUERY = "How many cars are in this image?"
JACKET_QUERY = "What color is the woman's jacket in this image?"
SODIUM_QUERY = "How much sodium is in this product?"
FASHION_QUERY = "Analyze this outfit"
SIMILARITY_THRESHOLD = 0.8
