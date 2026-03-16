# --- DEPENDENCIAS ---
from config.vision_multimodal_config import DEFAULT_ASSISTANT_PROMPT
from models.vision_demo_model import build_vision_demo_model
from orchestration.vision_image_orchestration import create_vision_message

# --- QUERY ---
def generate_model_response(
    encoded_image: str,
    user_query: str,
    assistant_prompt: str = DEFAULT_ASSISTANT_PROMPT,
) -> str:
    prompt = assistant_prompt + user_query
    messages = create_vision_message(prompt, encoded_image)
    response = build_vision_demo_model().chat(messages=messages)
    return response["choices"][0]["message"]["content"]


def generate_image_captions(
    encoded_images: list[str],
    user_query: str = "Describe the photo",
    assistant_prompt: str = DEFAULT_ASSISTANT_PROMPT,
) -> list[str]:
    return [
        generate_model_response(encoded_image, user_query, assistant_prompt)
        for encoded_image in encoded_images
    ]


def generate_nutrition_response(encoded_image: str, user_query: str) -> str:
    assistant_prompt = """
You are an expert nutritionist. Your task is to analyze the food items displayed in the image and provide a detailed nutritional assessment.
Follow this format.
1. Identification.
2. Portion Size & Calorie Estimation.
3. Total Calories.
4. Nutrient Breakdown.
5. Health Evaluation.
6. Disclaimer.
"""
    return generate_model_response(encoded_image, user_query, assistant_prompt)


def generate_fashion_response(
    user_image_base64: str,
    matched_item: dict,
    all_items: list[dict],
    similarity_score: float,
    threshold: float = 0.8,
) -> str:
    items_list = [
        f"- {item['Item Name']} (${item['Price']}): {item['Link']}" for item in all_items
    ]
    items_description = "\n".join(items_list)

    if similarity_score >= threshold:
        assistant_prompt = f"""
You're conducting a professional retail catalog analysis.
Focus exclusively on professional fashion analysis.
ITEM DETAILS
{items_description}
Please identify and describe clothing items objectively.
Please categorize the overall style.
Please include the ITEM DETAILS section at the end.
"""
    else:
        assistant_prompt = f"""
You're conducting a professional retail catalog analysis.
Focus exclusively on professional fashion analysis.
SIMILAR ITEMS
{items_description}
Please note these are similar but not exact items.
Please identify clothing elements objectively.
Please include the SIMILAR ITEMS section at the end.
"""

    return generate_model_response(user_image_base64, "Analyze this outfit", assistant_prompt)
