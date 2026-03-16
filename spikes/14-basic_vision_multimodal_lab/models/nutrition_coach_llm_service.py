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
        try:
            return self.response_generator(self.model_name, prompt, encoded_image)
        except Exception as exc:
            logger.error("Error generating nutrition response: %s", str(exc))
            return f"Error generating response: {exc}"

    def build_fallback_response(self, related_items) -> str:
        total_calories = int(related_items["Calories"].sum())
        lines = [
            "**Identification**",
            build_identification_lines(related_items),
            "",
            "**Portion Size & Calorie Estimation**",
            build_calorie_breakdown_lines(related_items),
            "",
            "**Total Calories**",
            f"Total Calories: {total_calories}",
            "",
            "**Nutrient Breakdown**",
            build_nutrient_breakdown_lines(related_items),
            "",
            "**Health Evaluation**",
            (
                "This estimate is grounded in the local nutrition catalog and suggests a balanced reading of "
                "the visible meal components."
            ),
            "",
            "**Disclaimer**",
            (
                "The nutritional information and calorie estimates provided are approximate and are based on "
                "general food data. Actual values may vary depending on factors such as portion size specific "
                "ingredients preparation methods and individual variations. For precise dietary advice or "
                "medical guidance consult a qualified nutritionist or healthcare provider."
            ),
        ]
        return "\n".join(lines)

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
        response = self.generate_response(user_image_base64, prompt)

        if response.startswith("Error generating response:") or len(response) < 120:
            return self.build_fallback_response(related_items)

        if "**Disclaimer**" not in response and "Disclaimer" not in response:
            response += (
                "\n\n**Disclaimer**\n"
                "The nutritional information and calorie estimates provided are approximate and are based on general food data. Actual values may vary depending on factors such as portion size specific ingredients preparation methods and individual variations. For precise dietary advice or medical guidance consult a qualified nutritionist or healthcare provider."
            )

        return response
