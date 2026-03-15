# --- DEPENDENCIAS ---
# 1. Sys: Para anadir la ruta del spike a los imports de prueba.
# 2. Path: Para resolver la ruta absoluta del spike.
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPIKE = ROOT / "spikes" / "14-basic_vision_multimodal_lab"

if str(SPIKE) not in sys.path:
    sys.path.insert(0, str(SPIKE))

from config.vision_multimodal_config import CAR_COUNT_QUERY
from config.vision_multimodal_config import CITY_SCENE_URL
from config.vision_multimodal_config import DEFAULT_VISION_QUERY
from config.vision_multimodal_config import FASHION_IMAGE_URL
from config.vision_multimodal_config import JACKET_QUERY
from config.vision_multimodal_config import NUTRITION_LABEL_URL
from config.vision_multimodal_config import SODIUM_QUERY
from orchestration.vision_image_orchestration import create_vision_message
from orchestration.vision_image_orchestration import encode_image_from_url
from orchestration.vision_query_orchestration import generate_fashion_response
from orchestration.vision_query_orchestration import generate_model_response
from orchestration.vision_query_orchestration import generate_nutrition_response
from orchestration.vision_similarity_orchestration import build_catalog_dataset
from orchestration.vision_similarity_orchestration import build_image_vector
from orchestration.vision_similarity_orchestration import find_closest_match


def test_create_vision_message_builds_text_and_image_parts():
    encoded_image = encode_image_from_url(CITY_SCENE_URL)
    messages = create_vision_message("Describe the photo", encoded_image)

    assert messages[0]["role"] == "user"
    assert messages[0]["content"][0]["type"] == "text"
    assert messages[0]["content"][1]["type"] == "image_url"
    assert messages[0]["content"][1]["image_url"]["url"].startswith("data:image/jpeg;base64,")


def test_general_image_query_returns_city_description():
    encoded_image = encode_image_from_url(CITY_SCENE_URL)
    response = generate_model_response(encoded_image, DEFAULT_VISION_QUERY)

    assert "city street" in response.lower()
    assert "three cars" in response.lower()


def test_object_count_and_attribute_questions_return_expected_answers():
    encoded_image = encode_image_from_url(CITY_SCENE_URL)

    car_response = generate_model_response(encoded_image, CAR_COUNT_QUERY)
    jacket_response = generate_model_response(encoded_image, JACKET_QUERY)

    assert "3 cars" in car_response.lower()
    assert "red" in jacket_response.lower()


def test_nutrition_response_mentions_sodium_and_calories():
    encoded_image = encode_image_from_url(NUTRITION_LABEL_URL)
    response = generate_nutrition_response(encoded_image, SODIUM_QUERY)

    assert "470 mg" in response.lower()
    assert "230 calories" in response.lower()
    assert "disclaimer" in response.lower()


def test_similarity_match_returns_expected_catalog_item():
    encoded_image = encode_image_from_url(FASHION_IMAGE_URL)
    dataset = build_catalog_dataset()
    matched_item, similarity_score = find_closest_match(build_image_vector(encoded_image), dataset)

    assert matched_item["Item Name"] == "Navy blazer with white blouse and black trousers"
    assert similarity_score > 0.9


def test_fashion_response_includes_catalog_section():
    encoded_image = encode_image_from_url(FASHION_IMAGE_URL)
    dataset = build_catalog_dataset()
    matched_item, similarity_score = find_closest_match(build_image_vector(encoded_image), dataset)
    response = generate_fashion_response(encoded_image, matched_item, dataset, similarity_score)

    assert "business casual" in response.lower()
    assert "catalog" in response.lower() or "item details" in response.lower()
    assert matched_item["Item Name"] in response
