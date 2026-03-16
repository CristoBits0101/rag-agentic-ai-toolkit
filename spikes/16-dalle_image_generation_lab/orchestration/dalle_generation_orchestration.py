# --- DEPENDENCIAS ---
import base64
from dataclasses import dataclass
from pathlib import Path

from config.dalle_image_generation_config import DALL_E_2_DEFAULT_COUNT
from config.dalle_image_generation_config import DALL_E_2_DEFAULT_SIZE
from config.dalle_image_generation_config import DALL_E_2_GALLERY_COUNT
from config.dalle_image_generation_config import DALL_E_2_MODEL_NAME
from config.dalle_image_generation_config import DALL_E_2_OUTPUT_FILE_NAME
from config.dalle_image_generation_config import DALL_E_2_SUPPORTED_SIZES
from config.dalle_image_generation_config import DALL_E_3_DEFAULT_COUNT
from config.dalle_image_generation_config import DALL_E_3_DEFAULT_QUALITY
from config.dalle_image_generation_config import DALL_E_3_DEFAULT_SIZE
from config.dalle_image_generation_config import DALL_E_3_MODEL_NAME
from config.dalle_image_generation_config import DALL_E_3_OUTPUT_FILE_NAME
from config.dalle_image_generation_config import DALL_E_3_SUPPORTED_QUALITIES
from config.dalle_image_generation_config import DALL_E_3_SUPPORTED_SIZES
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


@dataclass(frozen=True)
class DalleBatchGenerationResult:
    model_name: str
    prompt: str
    output_paths: tuple[Path, ...]


def build_dalle_2_request(prompt: str) -> DalleGenerationContext:
    return build_custom_dalle_2_request(prompt)


def build_custom_dalle_2_request(
    prompt: str,
    size: str = DALL_E_2_DEFAULT_SIZE,
    n: int = DALL_E_2_DEFAULT_COUNT,
    response_format: str = "b64_json",
) -> DalleGenerationContext:
    if size not in DALL_E_2_SUPPORTED_SIZES:
        raise ValueError(f"Unsupported DALL-E 2 size: {size}")

    if n < 1:
        raise ValueError("DALL-E 2 image count must be at least 1.")

    return DalleGenerationContext(
        model_name=DALL_E_2_MODEL_NAME,
        prompt=prompt,
        size=size,
        n=n,
        quality=None,
        response_format=response_format,
    )


def build_dalle_3_request(prompt: str) -> DalleGenerationContext:
    return build_custom_dalle_3_request(prompt)


def build_custom_dalle_3_request(
    prompt: str,
    size: str = DALL_E_3_DEFAULT_SIZE,
    quality: str = DALL_E_3_DEFAULT_QUALITY,
    response_format: str = "b64_json",
) -> DalleGenerationContext:
    if size not in DALL_E_3_SUPPORTED_SIZES:
        raise ValueError(f"Unsupported DALL-E 3 size: {size}")

    if quality not in DALL_E_3_SUPPORTED_QUALITIES:
        raise ValueError(f"Unsupported DALL-E 3 quality: {quality}")

    return DalleGenerationContext(
        model_name=DALL_E_3_MODEL_NAME,
        prompt=prompt,
        size=size,
        n=DALL_E_3_DEFAULT_COUNT,
        quality=quality,
        response_format=response_format,
    )


def extract_b64_image_payload(response) -> str:
    return extract_all_b64_image_payloads(response)[0]


def extract_all_b64_image_payloads(response) -> tuple[str, ...]:
    data = getattr(response, "data", None)
    if not data:
        raise RuntimeError("OpenAI image response did not contain data.")

    payloads = []
    for item in data:
        b64_payload = getattr(item, "b64_json", None)
        if b64_payload:
            payloads.append(b64_payload)
            continue

        if isinstance(item, dict) and item.get("b64_json"):
            payloads.append(item["b64_json"])

    if not payloads:
        raise RuntimeError("OpenAI image response did not contain b64_json.")

    return tuple(payloads)


def save_generated_image(image_b64: str, output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(base64.b64decode(image_b64))
    return path


def save_generated_images(
    image_payloads: tuple[str, ...] | list[str],
    output_dir: str | Path,
    file_prefix: str,
) -> tuple[Path, ...]:
    base_dir = Path(output_dir)
    base_dir.mkdir(parents=True, exist_ok=True)
    output_paths = []

    for index, payload in enumerate(image_payloads, start=1):
        output_path = base_dir / f"{file_prefix}_{index}.png"
        output_path.write_bytes(base64.b64decode(payload))
        output_paths.append(output_path)

    return tuple(output_paths)


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


def generate_image_batch_with_openai(
    generation_context: DalleGenerationContext,
    output_dir: str | Path,
    file_prefix: str,
    client_builder=build_openai_image_client,
) -> DalleBatchGenerationResult:
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
    output_paths = save_generated_images(
        extract_all_b64_image_payloads(response),
        output_dir,
        file_prefix,
    )
    return DalleBatchGenerationResult(
        model_name=generation_context.model_name,
        prompt=generation_context.prompt,
        output_paths=output_paths,
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


def build_dalle_2_gallery_request(prompt: str = DEFAULT_CAT_PROMPT) -> DalleGenerationContext:
    return build_custom_dalle_2_request(
        prompt=prompt,
        size=DALL_E_2_DEFAULT_SIZE,
        n=DALL_E_2_GALLERY_COUNT,
    )
