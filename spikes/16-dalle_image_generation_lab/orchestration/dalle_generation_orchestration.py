# --- DEPENDENCIAS ---
import base64
from dataclasses import dataclass
from pathlib import Path

from config.dalle_image_generation_config import DALL_E_2_DEFAULT_COUNT
from config.dalle_image_generation_config import DALL_E_2_DEFAULT_SIZE
from config.dalle_image_generation_config import DALL_E_2_MODEL_NAME
from config.dalle_image_generation_config import DALL_E_2_OUTPUT_FILE_NAME
from config.dalle_image_generation_config import DALL_E_3_DEFAULT_COUNT
from config.dalle_image_generation_config import DALL_E_3_DEFAULT_QUALITY
from config.dalle_image_generation_config import DALL_E_3_DEFAULT_SIZE
from config.dalle_image_generation_config import DALL_E_3_MODEL_NAME
from config.dalle_image_generation_config import DALL_E_3_OUTPUT_FILE_NAME
from config.dalle_image_generation_config import DEFAULT_CAT_PROMPT
from config.dalle_image_generation_config import OUTPUTS_DIR
from models.dalle_openai_gateway import build_openai_image_client

# --- IMAGE ---
@dataclass(frozen=True)
class DalleGenerationContext:
    model_name: str
    prompt: str
    size: str
    n: int
    quality: str | None
    response_format: str


@dataclass(frozen=True)
class DalleGenerationResult:
    model_name: str
    prompt: str
    output_path: Path


def build_dalle_2_request(prompt: str) -> DalleGenerationContext:
    return DalleGenerationContext(
        model_name=DALL_E_2_MODEL_NAME,
        prompt=prompt,
        size=DALL_E_2_DEFAULT_SIZE,
        n=DALL_E_2_DEFAULT_COUNT,
        quality=None,
        response_format="b64_json",
    )


def build_dalle_3_request(prompt: str) -> DalleGenerationContext:
    return DalleGenerationContext(
        model_name=DALL_E_3_MODEL_NAME,
        prompt=prompt,
        size=DALL_E_3_DEFAULT_SIZE,
        n=DALL_E_3_DEFAULT_COUNT,
        quality=DALL_E_3_DEFAULT_QUALITY,
        response_format="b64_json",
    )


def extract_b64_image_payload(response) -> str:
    data = getattr(response, "data", None)
    if not data:
        raise RuntimeError("OpenAI image response did not contain data.")

    first_item = data[0]
    b64_payload = getattr(first_item, "b64_json", None)
    if b64_payload:
        return b64_payload

    if isinstance(first_item, dict) and first_item.get("b64_json"):
        return first_item["b64_json"]

    raise RuntimeError("OpenAI image response did not contain b64_json.")


def save_generated_image(image_b64: str, output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(base64.b64decode(image_b64))
    return path


def generate_image_with_openai(
    generation_context: DalleGenerationContext,
    output_path: str | Path,
    client_builder=build_openai_image_client,
) -> DalleGenerationResult:
    client = client_builder()
    generation_kwargs = {
        "model": generation_context.model_name,
        "prompt": generation_context.prompt,
        "size": generation_context.size,
        "n": generation_context.n,
        "response_format": generation_context.response_format,
    }

    if generation_context.quality:
        generation_kwargs["quality"] = generation_context.quality

    response = client.images.generate(**generation_kwargs)
    output_file = save_generated_image(extract_b64_image_payload(response), output_path)
    return DalleGenerationResult(
        model_name=generation_context.model_name,
        prompt=generation_context.prompt,
        output_path=output_file,
    )


def generate_default_dalle_2_cat_image(
    output_path: str | Path = OUTPUTS_DIR / DALL_E_2_OUTPUT_FILE_NAME,
    client_builder=build_openai_image_client,
) -> DalleGenerationResult:
    return generate_image_with_openai(
        build_dalle_2_request(DEFAULT_CAT_PROMPT),
        output_path,
        client_builder=client_builder,
    )


def generate_default_dalle_3_cat_image(
    output_path: str | Path = OUTPUTS_DIR / DALL_E_3_OUTPUT_FILE_NAME,
    client_builder=build_openai_image_client,
) -> DalleGenerationResult:
    return generate_image_with_openai(
        build_dalle_3_request(DEFAULT_CAT_PROMPT),
        output_path,
        client_builder=client_builder,
    )
