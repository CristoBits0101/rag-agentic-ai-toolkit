# --- DEPENDENCIAS ---
import logging

from models.vision_ollama_gateway import generate_ollama_vision_response_from_base64

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class StyleFinderVisionService:
    def __init__(self, model_name: str, response_generator=generate_ollama_vision_response_from_base64):
        self.model_name = model_name
        self.response_generator = response_generator

    def generate_response(self, encoded_image, prompt):
        logger.info("Sending request to model %s with prompt length %d", self.model_name, len(prompt))
        content = self.response_generator(self.model_name, prompt, encoded_image)
        logger.info("Received response with length %d", len(content))
        return content

    def generate_fashion_response(
        self,
        user_image_base64,
        matched_row,
        all_items,
        similarity_score,
        threshold=0.8,
    ):
        items_description = "\n".join(
            [
                f"- {row['Item Name']} (${row['Price']:.2f}): {row['Link']}"
                for _, row in all_items.iterrows()
            ]
        )

        if similarity_score >= threshold:
            assistant_prompt = (
                "You are conducting a professional retail catalog analysis. "
                f"The matched look is {matched_row['Look Title']} with style {matched_row['Style']}. "
                "Focus exclusively on professional fashion analysis for a clothing retailer. "
                f"ITEM DETAILS:\n{items_description}\n\n"
                "Please identify the clothing objectively by color cut and styling cues. "
                "Categorize the overall look. "
                "Always include the ITEM DETAILS section at the end."
            )
        else:
            assistant_prompt = (
                "You are conducting a professional retail catalog analysis. "
                f"The matched look is {matched_row['Look Title']} with style {matched_row['Style']}. "
                "Focus exclusively on professional fashion analysis for a clothing retailer. "
                f"SIMILAR ITEMS:\n{items_description}\n\n"
                "Please explain that the items are visually similar but not exact. "
                "Describe the clothing objectively by color cut and styling cues. "
                "Always include the SIMILAR ITEMS section at the end."
            )

        try:
            response = self.generate_response(user_image_base64, assistant_prompt)
        except Exception as exc:
            logger.error("Error generating fashion response: %s", str(exc))
            return f"Error generating response: {exc}"

        section_header = "ITEM DETAILS:" if similarity_score >= threshold else "SIMILAR ITEMS:"

        if len(response) < 100:
            return (
                "Error generating response: Ollama returned an incomplete fashion analysis.\n\n"
                f"{section_header}\n{items_description}"
            )

        if "ITEM DETAILS:" not in response and "SIMILAR ITEMS:" not in response:
            response += f"\n\n{section_header}\n{items_description}"

        return response
