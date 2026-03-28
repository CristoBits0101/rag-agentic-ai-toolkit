# --- DEPENDENCIAS ---
# 1. Sys: Para anadir la ruta del spike a los imports de prueba.
# 2. Path: Para resolver la ruta absoluta del spike.
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPIKE = ROOT / "spikes" / "14-vision_multimodal"

if str(SPIKE) not in sys.path:
    sys.path.insert(0, str(SPIKE))

from config.vision_real_provider_config import LLAMA32_VISION_MODEL_NAME
from config.vision_real_provider_config import LLAVA_MODEL_NAME
from config.vision_real_provider_config import QWEN25_VL_MODEL_NAME
from config.vision_real_provider_config import REAL_CITY_SCENE_IMAGE_PATH
from config.vision_real_provider_config import REAL_NUTRITION_LABEL_IMAGE_PATH
from models.vision_ollama_gateway import build_ollama_vision_payload_from_base64
from models.vision_ollama_gateway import build_ollama_vision_payload
from models.vision_ollama_gateway import encode_real_image_file
from models.vision_ollama_gateway import extract_ollama_vision_text
from orchestration import vision_real_variants_orchestration as real_variants


def test_encode_real_image_file_returns_base64_text():
    encoded_image = encode_real_image_file(REAL_CITY_SCENE_IMAGE_PATH)

    assert encoded_image
    assert isinstance(encoded_image, str)


def test_build_ollama_vision_payload_includes_model_prompt_and_image():
    payload = build_ollama_vision_payload(
        model_name=LLAVA_MODEL_NAME,
        prompt="Describe the image.",
        image_path=REAL_CITY_SCENE_IMAGE_PATH,
    )

    assert payload["model"] == LLAVA_MODEL_NAME
    assert payload["stream"] is False
    assert payload["messages"][0]["content"] == "Describe the image."
    assert len(payload["messages"][0]["images"]) == 1


def test_build_ollama_vision_payload_from_base64_keeps_encoded_image():
    payload = build_ollama_vision_payload_from_base64(
        model_name=LLAVA_MODEL_NAME,
        prompt="Describe the image.",
        encoded_image="encoded-image",
    )

    assert payload["messages"][0]["images"] == ["encoded-image"]


def test_extract_ollama_vision_text_reads_message_content():
    response_payload = {"message": {"content": "There are three cars in the scene."}}

    assert extract_ollama_vision_text(response_payload) == "There are three cars in the scene."


def test_run_real_vision_variant_uses_shared_response_generator():
    run = real_variants.run_real_vision_variant(
        model_name=LLAVA_MODEL_NAME,
        image_path=REAL_CITY_SCENE_IMAGE_PATH,
        prompt="Describe the image.",
        response_generator=lambda model_name, prompt, image_path: f"{model_name} answered.",
    )

    assert run.model_name == LLAVA_MODEL_NAME
    assert run.image_path == REAL_CITY_SCENE_IMAGE_PATH
    assert run.response == f"{LLAVA_MODEL_NAME} answered."


def test_run_llava_example_uses_expected_defaults(monkeypatch):
    monkeypatch.setattr(
        real_variants,
        "generate_ollama_vision_response",
        lambda model_name, prompt, image_path: "LLaVA saw three cars.",
    )

    run = real_variants.run_llava_example()

    assert run.model_name == LLAVA_MODEL_NAME
    assert run.image_path == REAL_CITY_SCENE_IMAGE_PATH
    assert "cars" in run.response.lower()


def test_run_llama32_vision_example_uses_expected_defaults(monkeypatch):
    monkeypatch.setattr(
        real_variants,
        "generate_ollama_vision_response",
        lambda model_name, prompt, image_path: "Llama vision described the city scene.",
    )

    run = real_variants.run_llama32_vision_example()

    assert run.model_name == LLAMA32_VISION_MODEL_NAME
    assert run.image_path == REAL_CITY_SCENE_IMAGE_PATH
    assert "city" in run.response.lower()


def test_run_qwen25_vl_example_uses_expected_defaults(monkeypatch):
    monkeypatch.setattr(
        real_variants,
        "generate_ollama_vision_response",
        lambda model_name, prompt, image_path: "The sodium value appears to be 470 mg.",
    )

    run = real_variants.run_qwen25_vl_example()

    assert run.model_name == QWEN25_VL_MODEL_NAME
    assert run.image_path == REAL_NUTRITION_LABEL_IMAGE_PATH
    assert "470" in run.response


def test_real_vision_variant_subfolders_exist():
    assert (SPIKE / "llava_vision_querying" / "main.py").exists()
    assert (SPIKE / "llama3_2_vision_querying" / "main.py").exists()
    assert (SPIKE / "qwen2_5vl_vision_querying" / "main.py").exists()
