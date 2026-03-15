# --- DEPENDENCIAS ---
from dataclasses import dataclass
from pathlib import Path

from config.vision_real_provider_config import LLAMA32_VISION_MODEL_NAME
from config.vision_real_provider_config import LLAVA_MODEL_NAME
from config.vision_real_provider_config import QWEN25_VL_MODEL_NAME
from config.vision_real_provider_config import REAL_CITY_SCENE_IMAGE_PATH
from config.vision_real_provider_config import REAL_CITY_SCENE_QUERY
from config.vision_real_provider_config import REAL_NUTRITION_LABEL_IMAGE_PATH
from config.vision_real_provider_config import REAL_NUTRITION_QUERY
from models.vision_ollama_gateway import generate_ollama_vision_response

# --- QUERY ---
@dataclass(frozen=True)
class RealVisionVariantRun:
    model_name: str
    image_path: Path
    prompt: str
    response: str


def run_real_vision_variant(
    model_name: str,
    image_path: str | Path,
    prompt: str,
    response_generator=None,
) -> RealVisionVariantRun:
    path = Path(image_path)
    if not path.exists():
        raise RuntimeError(f"The image path does not exist: {path}")

    generator = response_generator or generate_ollama_vision_response
    response = generator(model_name, prompt, path)
    return RealVisionVariantRun(
        model_name=model_name,
        image_path=path,
        prompt=prompt,
        response=response,
    )


def run_llava_example() -> RealVisionVariantRun:
    return run_real_vision_variant(
        model_name=LLAVA_MODEL_NAME,
        image_path=REAL_CITY_SCENE_IMAGE_PATH,
        prompt=REAL_CITY_SCENE_QUERY,
    )


def run_llama32_vision_example() -> RealVisionVariantRun:
    return run_real_vision_variant(
        model_name=LLAMA32_VISION_MODEL_NAME,
        image_path=REAL_CITY_SCENE_IMAGE_PATH,
        prompt=REAL_CITY_SCENE_QUERY,
    )


def run_qwen25_vl_example() -> RealVisionVariantRun:
    return run_real_vision_variant(
        model_name=QWEN25_VL_MODEL_NAME,
        image_path=REAL_NUTRITION_LABEL_IMAGE_PATH,
        prompt=REAL_NUTRITION_QUERY,
    )
