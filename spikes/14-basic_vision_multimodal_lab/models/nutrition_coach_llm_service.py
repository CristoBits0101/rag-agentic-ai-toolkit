# --- DEPENDENCIAS ---
import logging

from models.vision_ollama_gateway import generate_ollama_vision_response_from_base64
from orchestration.nutrition_coach_helpers import build_calorie_breakdown_lines
from orchestration.nutrition_coach_helpers import build_identification_lines
from orchestration.nutrition_coach_helpers import build_nutrition_reference_text
from orchestration.nutrition_coach_helpers import build_nutrient_breakdown_lines

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class NutritionCoachVisionService:
    def __init__(self, model_name: str, response_generator=generate_ollama_vision_response_from_base64):
        self.model_name = model_name
        self.response_generator = response_generator

    def generate_response(self, encoded_image: str, prompt: str) -> str:
        return self.response_generator(self.model_name, prompt, encoded_image)

    def generate_nutrition_response(
        self,
        user_image_base64: str,
        related_items,
        user_query: str,
    ) -> str:
        prompt = (
            "You are an expert nutritionist. Analyze the uploaded meal image and answer the user query. "
            "Use the retrieved nutrition context as authoritative reference.\n\n"
            f"Retrieved nutrition context:\n{build_nutrition_reference_text(related_items)}\n\n"
            "Return these sections in order.\n"
            "**Identification**\n"
            "**Portion Size & Calorie Estimation**\n"
            "**Total Calories**\n"
            "**Nutrient Breakdown**\n"
            "**Health Evaluation**\n"
            "**Disclaimer**\n\n"
            f"User query: {user_query}"
        )
        try:
            response = self.generate_response(user_image_base64, prompt)
        except Exception as exc:
            logger.error("Error generating nutrition response: %s", str(exc))
            return f"Error generating response: {exc}"

        if len(response) < 120:
            total_calories = int(related_items["Calories"].sum())
            return (
                "Error generating response: Ollama returned an incomplete nutrition analysis.\n\n"
                "**Reference Context**\n"
                f"{build_identification_lines(related_items)}\n\n"
                "**Estimated Total Calories**\n"
                f"Total Calories: {total_calories}\n\n"
                "**Reference Nutrients**\n"
                f"{build_nutrient_breakdown_lines(related_items)}"
            )

        if "**Disclaimer**" not in response and "Disclaimer" not in response:
            response += (
                "\n\n**Disclaimer**\n"
                "The nutritional information and calorie estimates provided are approximate and are based on general food data. Actual values may vary depending on factors such as portion size specific ingredients preparation methods and individual variations. For precise dietary advice or medical guidance consult a qualified nutritionist or healthcare provider."
            )

        return response
