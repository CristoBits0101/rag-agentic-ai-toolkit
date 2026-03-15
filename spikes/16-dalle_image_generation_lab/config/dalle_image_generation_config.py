# --- DEPENDENCIAS ---
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUTS_DIR = BASE_DIR / "outputs"
DEFAULT_CAT_PROMPT = "a white siamese cat"
EXERCISE_PROMPT = "a beautiful lake with a sunset"
DALL_E_2_MODEL_NAME = "dall-e-2"
DALL_E_3_MODEL_NAME = "dall-e-3"
DALL_E_2_DEFAULT_SIZE = "1024x1024"
DALL_E_3_DEFAULT_SIZE = "1024x1024"
DALL_E_3_DEFAULT_QUALITY = "standard"
DALL_E_2_DEFAULT_COUNT = 1
DALL_E_3_DEFAULT_COUNT = 1
DALL_E_2_OUTPUT_FILE_NAME = "dall_e_2_cat.png"
DALL_E_3_OUTPUT_FILE_NAME = "dall_e_3_cat.png"
DALL_E_2_EXERCISE_FILE_NAME = "dall_e_2_lake.png"
DALL_E_3_EXERCISE_FILE_NAME = "dall_e_3_lake.png"
