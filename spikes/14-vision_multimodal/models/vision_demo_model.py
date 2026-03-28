# --- DEPENDENCIAS ---
import base64
import json

from data.vision_sample_dataset import VISION_SAMPLE_RECORDS

# --- MODEL ---
def decode_sample_record(encoded_image: str):
    try:
        payload = base64.b64decode(encoded_image).decode("utf-8")
        image_payload = json.loads(payload)
        return VISION_SAMPLE_RECORDS.get(image_payload["image_id"])
    except Exception:
        return None


def extract_items_section(prompt: str) -> str:
    if "ITEM DETAILS" in prompt:
        section = prompt.split("ITEM DETAILS", maxsplit=1)[1]
        if "Please" in section:
            section = section.split("Please", maxsplit=1)[0]
        return section.strip()

    if "SIMILAR ITEMS" in prompt:
        section = prompt.split("SIMILAR ITEMS", maxsplit=1)[1]
        if "Please" in section:
            section = section.split("Please", maxsplit=1)[0]
        return section.strip()

    return ""


def build_general_response(record, prompt: str) -> str:
    lowered_prompt = prompt.lower()

    if "how many cars" in lowered_prompt:
        return f"There are {record.object_counts.get('cars', 0)} cars in the image."

    if "what color is the woman's jacket" in lowered_prompt:
        color = record.attributes.get("woman_jacket_color", "not clearly visible")
        return f"The woman's jacket appears to be {color}."

    if "how much sodium" in lowered_prompt:
        sodium = record.text_fields.get("sodium", "not available")
        return f"The nutrition label shows {sodium} of sodium."

    if "describe the photo" in lowered_prompt or "describe the image" in lowered_prompt:
        return record.description

    if "answer the following user query" in lowered_prompt:
        return record.description

    return record.description


def build_nutrition_response(record) -> str:
    calories = record.text_fields.get("calories", "unknown")
    sodium = record.text_fields.get("sodium", "unknown")
    protein = record.text_fields.get("protein", "unknown")
    carbohydrates = record.text_fields.get("carbohydrates", "unknown")
    fat = record.text_fields.get("fat", "unknown")
    vitamin_c = record.text_fields.get("vitamin_c", "unknown")

    return (
        "1. Identification:\n"
        "Nutrition label for a packaged food product.\n"
        "2. Portion Size & Calorie Estimation:\n"
        f"* Product serving: 1 serving, {calories} calories\n"
        f"3. Total Calories:\nTotal Calories: {calories} calories\n"
        "4. Nutrient Breakdown:\n"
        f"* Protein: {protein}\n"
        f"* Carbohydrates: {carbohydrates}\n"
        f"* Fats: {fat}\n"
        f"* Minerals: Sodium {sodium}\n"
        f"* Vitamins: Vitamin C {vitamin_c}\n"
        "5. Health Evaluation:\n"
        "This label suggests a moderate calorie packaged food item with meaningful sodium content so portion awareness is important.\n"
        "6. Disclaimer:\n"
        "The nutritional information and calorie estimates provided are approximate and are based on general food data. "
        "Actual values may vary depending on factors such as portion size specific ingredients preparation methods and individual variations. "
        "For precise dietary advice or medical guidance consult a qualified nutritionist or healthcare provider."
    )


def build_fashion_response(record, prompt: str) -> str:
    items_section = extract_items_section(prompt)
    style = record.attributes.get("style", "unknown style")
    outerwear = record.attributes.get("outerwear", "outerwear not detected")
    top = record.attributes.get("top", "top not detected")
    bottom = record.attributes.get("bottom", "bottom not detected")

    prefix = "These appear to be similar items rather than an exact match." if "SIMILAR ITEMS" in prompt else "This appears to be a strong catalog match."

    return (
        f"{prefix} "
        f"The outfit is best described as {style}. "
        f"The visible clothing elements include {outerwear} {top} and {bottom}. "
        "The presentation is objective and suitable for retail catalog analysis.\n\n"
        f"{items_section}"
    )


class VisionDemoModel:
    def chat(self, messages):
        content = messages[0]["content"]
        prompt = next(part["text"] for part in content if part["type"] == "text")
        image_url = next(part["image_url"]["url"] for part in content if part["type"] == "image_url")
        encoded_image = image_url.split(",", maxsplit=1)[1]
        record = decode_sample_record(encoded_image)

        if not record:
            answer = "The image could not be interpreted by the local demo model."
        elif "expert nutritionist" in prompt.lower():
            answer = build_nutrition_response(record)
        elif "professional retail catalog analysis" in prompt.lower():
            answer = build_fashion_response(record, prompt)
        else:
            answer = build_general_response(record, prompt)

        return {"choices": [{"message": {"content": answer}}]}


def build_vision_demo_model() -> VisionDemoModel:
    return VisionDemoModel()
