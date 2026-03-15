# --- DEPENDENCIAS ---
# 1. Sys: Para anadir la ruta del spike a los imports de prueba.
# 2. Path: Para resolver la ruta absoluta del spike.
import base64
import sys
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[2]
SPIKE = ROOT / "spikes" / "16-dalle_image_generation_lab"

if str(SPIKE) not in sys.path:
    sys.path.insert(0, str(SPIKE))

from config.dalle_image_generation_config import DALL_E_2_MODEL_NAME
from config.dalle_image_generation_config import DALL_E_3_MODEL_NAME
from config.dalle_image_generation_config import DALL_E_3_DEFAULT_QUALITY
from config.dalle_image_generation_config import DEFAULT_CAT_PROMPT
from orchestration.dalle_generation_orchestration import build_dalle_2_request
from orchestration.dalle_generation_orchestration import build_dalle_3_request
from orchestration.dalle_generation_orchestration import extract_b64_image_payload
from orchestration.dalle_generation_orchestration import generate_default_dalle_2_cat_image
from orchestration.dalle_generation_orchestration import generate_default_dalle_3_cat_image
from orchestration.dalle_generation_orchestration import save_generated_image


def build_fake_image_response(image_bytes: bytes):
    return SimpleNamespace(
        data=[
            SimpleNamespace(
                b64_json=base64.b64encode(image_bytes).decode("utf-8"),
            )
        ]
    )


def build_fake_openai_client(image_bytes: bytes):
    fake_response = build_fake_image_response(image_bytes)
    fake_images = SimpleNamespace(generate=lambda **kwargs: fake_response)
    return SimpleNamespace(images=fake_images)


def test_build_dalle_2_request_uses_expected_defaults():
    context = build_dalle_2_request(DEFAULT_CAT_PROMPT)

    assert context.model_name == DALL_E_2_MODEL_NAME
    assert context.prompt == DEFAULT_CAT_PROMPT
    assert context.quality is None


def test_build_dalle_3_request_uses_expected_defaults():
    context = build_dalle_3_request(DEFAULT_CAT_PROMPT)

    assert context.model_name == DALL_E_3_MODEL_NAME
    assert context.prompt == DEFAULT_CAT_PROMPT
    assert context.quality == DALL_E_3_DEFAULT_QUALITY


def test_extract_b64_image_payload_reads_first_item():
    response = build_fake_image_response(b"png-image")

    payload = extract_b64_image_payload(response)

    assert base64.b64decode(payload) == b"png-image"


def test_save_generated_image_writes_png_bytes(tmp_path):
    output_path = tmp_path / "generated.png"
    saved_path = save_generated_image(base64.b64encode(b"png-image").decode("utf-8"), output_path)

    assert saved_path == output_path
    assert output_path.read_bytes() == b"png-image"


def test_generate_default_dalle_2_cat_image_uses_fake_client(tmp_path):
    result = generate_default_dalle_2_cat_image(
        output_path=tmp_path / "dalle2.png",
        client_builder=lambda: build_fake_openai_client(b"dalle-2-image"),
    )

    assert result.model_name == DALL_E_2_MODEL_NAME
    assert result.prompt == DEFAULT_CAT_PROMPT
    assert result.output_path.read_bytes() == b"dalle-2-image"


def test_generate_default_dalle_3_cat_image_uses_fake_client(tmp_path):
    result = generate_default_dalle_3_cat_image(
        output_path=tmp_path / "dalle3.png",
        client_builder=lambda: build_fake_openai_client(b"dalle-3-image"),
    )

    assert result.model_name == DALL_E_3_MODEL_NAME
    assert result.prompt == DEFAULT_CAT_PROMPT
    assert result.output_path.read_bytes() == b"dalle-3-image"


def test_dalle_variant_subfolders_exist():
    assert (SPIKE / "dall_e_2_generation" / "main.py").exists()
    assert (SPIKE / "dall_e_3_generation" / "main.py").exists()
