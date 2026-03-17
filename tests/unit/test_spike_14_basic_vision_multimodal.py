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
from config.vision_multimodal_config import CAT_IMAGE_URL
from config.vision_multimodal_config import CITY_SCENE_URL
from config.vision_multimodal_config import DEFAULT_ASSISTANT_PROMPT
from config.vision_multimodal_config import DEFAULT_VISION_QUERY
from config.vision_multimodal_config import FASHION_IMAGE_URL
from config.vision_multimodal_config import JACKET_QUERY
from config.vision_multimodal_config import NUTRITION_LABEL_URL
from config.vision_multimodal_config import SODIUM_QUERY
from orchestration.vision_image_orchestration import create_vision_message
from orchestration.vision_image_orchestration import encode_images_from_urls
from orchestration.vision_image_orchestration import encode_image_from_url
from orchestration.vision_query_orchestration import generate_fashion_response
from orchestration.vision_query_orchestration import generate_image_captions
from orchestration.vision_query_orchestration import generate_model_response
from orchestration.vision_query_orchestration import generate_nutrition_response
from orchestration.vision_similarity_orchestration import build_catalog_dataset
from orchestration.vision_similarity_orchestration import build_image_vector
from orchestration.vision_similarity_orchestration import find_closest_match


def fake_vision_response_generator(model_name: str, prompt: str, encoded_image: str) -> str:
    lowered_prompt = prompt.lower()
    if "how many cars" in lowered_prompt:
        return "There are 3 cars in the image."
    if "what color is the woman's jacket" in lowered_prompt:
        return "The woman's jacket appears to be red."
    if "how much sodium" in lowered_prompt:
        return "The nutrition label shows 470 mg of sodium and 230 calories."
    if "professional retail catalog analysis" in lowered_prompt:
        return (
            "The outfit reads as business casual.\n\n"
            "ITEM DETAILS:\n- Navy blazer with white blouse and black trousers"
        )
    if "describe the photo" in lowered_prompt or "describe the image" in lowered_prompt:
        return "The photo shows a city street with three cars near a crosswalk."
    return "The image was analyzed with a real vision gateway."


def test_create_vision_message_builds_text_and_image_parts():
    encoded_image = encode_image_from_url(CITY_SCENE_URL)
    messages = create_vision_message("Describe the photo", encoded_image)

    assert messages[0]["role"] == "user"
    assert messages[0]["content"][0]["type"] == "text"
    assert messages[0]["content"][1]["type"] == "image_url"
    assert messages[0]["content"][1]["image_url"]["url"].startswith("data:image/jpeg;base64,")


def test_general_image_query_returns_city_description():
    encoded_image = encode_image_from_url(CITY_SCENE_URL)
    response = generate_model_response(
        encoded_image,
        DEFAULT_VISION_QUERY,
        response_generator=fake_vision_response_generator,
    )

    assert "city street" in response.lower()
    assert "cars" in response.lower()


def test_generate_image_captions_returns_one_caption_per_image():
    encoded_images = encode_images_from_urls([CAT_IMAGE_URL, CITY_SCENE_URL])
    from orchestration import vision_query_orchestration as query_orchestration

    original_generator = query_orchestration.generate_model_response
    query_orchestration.generate_model_response = (
        lambda encoded_image, user_query, assistant_prompt=DEFAULT_ASSISTANT_PROMPT: fake_vision_response_generator(
            "qwen2.5vl:3b",
            assistant_prompt + user_query,
            encoded_image,
        )
    )
    captions = generate_image_captions(encoded_images)
    query_orchestration.generate_model_response = original_generator

    assert len(captions) == 2
    assert "city street" in captions[0].lower()
    assert "city street" in captions[1].lower()


def test_object_count_and_attribute_questions_return_expected_answers():
    encoded_image = encode_image_from_url(CITY_SCENE_URL)

    car_response = generate_model_response(
        encoded_image,
        CAR_COUNT_QUERY,
        response_generator=fake_vision_response_generator,
    )
    jacket_response = generate_model_response(
        encoded_image,
        JACKET_QUERY,
        response_generator=fake_vision_response_generator,
    )

    assert "3 cars" in car_response.lower()
    assert "red" in jacket_response.lower()


def test_nutrition_response_mentions_sodium_and_calories():
    encoded_image = encode_image_from_url(NUTRITION_LABEL_URL)
    from orchestration import vision_query_orchestration as query_orchestration

    original_generator = query_orchestration.generate_model_response
    query_orchestration.generate_model_response = (
        lambda encoded_image, user_query, assistant_prompt=DEFAULT_ASSISTANT_PROMPT: fake_vision_response_generator(
            "qwen2.5vl:3b",
            assistant_prompt + user_query,
            encoded_image,
        )
    )
    response = generate_nutrition_response(encoded_image, SODIUM_QUERY)
    query_orchestration.generate_model_response = original_generator

    assert "470 mg" in response.lower()
    assert "230 calories" in response.lower()


def test_similarity_match_returns_expected_catalog_item():
    encoded_image = encode_image_from_url(FASHION_IMAGE_URL)
    dataset = build_catalog_dataset()
    matched_item, similarity_score = find_closest_match(build_image_vector(encoded_image), dataset)

    assert matched_item["Item Name"]
    assert similarity_score >= 0.0


def test_fashion_response_includes_catalog_section():
    encoded_image = encode_image_from_url(FASHION_IMAGE_URL)
    dataset = build_catalog_dataset()
    matched_item, similarity_score = find_closest_match(build_image_vector(encoded_image), dataset)
    from orchestration import vision_query_orchestration as query_orchestration

    original_generator = query_orchestration.generate_model_response
    query_orchestration.generate_model_response = (
        lambda encoded_image, user_query, assistant_prompt=DEFAULT_ASSISTANT_PROMPT: fake_vision_response_generator(
            "qwen2.5vl:3b",
            assistant_prompt + user_query,
            encoded_image,
        )
    )
    response = generate_fashion_response(encoded_image, matched_item, dataset, similarity_score)
    query_orchestration.generate_model_response = original_generator

    assert isinstance(response, str)
    assert "catalog" in response.lower() or "item details" in response.lower()
