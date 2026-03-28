# --- DEPENDENCIAS ---
from config.vision_multimodal_config import CAT_IMAGE_URL
from config.vision_multimodal_config import CAR_COUNT_QUERY
from config.vision_multimodal_config import CITY_SCENE_URL
from config.vision_multimodal_config import DEFAULT_VISION_QUERY
from config.vision_multimodal_config import FASHION_IMAGE_URL
from config.vision_multimodal_config import JACKET_QUERY
from config.vision_multimodal_config import NUTRITION_LABEL_URL
from config.vision_multimodal_config import SIMILARITY_THRESHOLD
from config.vision_multimodal_config import SODIUM_QUERY
from orchestration.vision_image_orchestration import encode_images_from_urls
from orchestration.vision_image_orchestration import encode_image_from_url
from orchestration.vision_query_orchestration import generate_image_captions
from orchestration.vision_query_orchestration import generate_fashion_response
from orchestration.vision_query_orchestration import generate_model_response
from orchestration.vision_query_orchestration import generate_nutrition_response
from orchestration.vision_similarity_orchestration import build_catalog_dataset
from orchestration.vision_similarity_orchestration import build_image_vector
from orchestration.vision_similarity_orchestration import find_closest_match


def print_separator(title: str) -> None:
    print("=" * 60)
    print(title)
    print("=" * 60)


def run_basic_vision_multimodal_lab() -> None:
    print_separator("14. BASIC VISION MULTIMODAL LAB")

    city_image = encode_image_from_url(CITY_SCENE_URL)
    fashion_image = encode_image_from_url(FASHION_IMAGE_URL)
    nutrition_image = encode_image_from_url(NUTRITION_LABEL_URL)

    print("General Query:")
    print(generate_model_response(city_image, DEFAULT_VISION_QUERY))
    print()

    print("Batch Image Captioning:")
    for index, caption in enumerate(
        generate_image_captions(
            encode_images_from_urls([CAT_IMAGE_URL, CITY_SCENE_URL]),
            DEFAULT_VISION_QUERY,
        ),
        start=1,
    ):
        print(f"Image {index}: {caption}")
    print()

    print("Object Count:")
    print(generate_model_response(city_image, CAR_COUNT_QUERY))
    print()

    print("Visual Attribute:")
    print(generate_model_response(city_image, JACKET_QUERY))
    print()

    print("Nutrition Analysis:")
    print(generate_nutrition_response(nutrition_image, SODIUM_QUERY))
    print()

    catalog_dataset = build_catalog_dataset()
    matched_item, similarity_score = find_closest_match(
        build_image_vector(fashion_image),
        catalog_dataset,
    )

    print("Fashion Similarity Match:")
    print(f"Matched Item: {matched_item['Item Name']}")
    print(f"Similarity Score: {similarity_score:.3f}")
    print()

    print("Fashion Analysis:")
    print(
        generate_fashion_response(
            fashion_image,
            matched_item,
            catalog_dataset,
            similarity_score,
            threshold=SIMILARITY_THRESHOLD,
        )
    )
