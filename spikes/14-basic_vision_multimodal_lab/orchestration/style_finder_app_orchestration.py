# --- DEPENDENCIAS ---
import os
from pathlib import Path
from tempfile import NamedTemporaryFile

from config.style_finder_fashion_config import STYLE_FINDER_DEFAULT_MODEL
from config.style_finder_fashion_config import STYLE_FINDER_IMAGE_SIZE
from config.style_finder_fashion_config import STYLE_FINDER_SIMILARITY_THRESHOLD
from models.style_finder_image_processor import StyleFinderImageProcessor
from models.style_finder_llm_service import StyleFinderVisionService
from orchestration.style_finder_asset_orchestration import ensure_style_finder_example_assets
from orchestration.style_finder_dataset_orchestration import build_style_finder_dataset
from orchestration.style_finder_helpers import build_alternatives_map
from orchestration.style_finder_helpers import format_alternatives_response
from orchestration.style_finder_helpers import get_all_items_for_image
from orchestration.style_finder_helpers import process_response


class StyleFinderApp:
    def __init__(
        self,
        model_name: str = STYLE_FINDER_DEFAULT_MODEL,
        image_processor=None,
        llm_service_factory=StyleFinderVisionService,
        dataset_builder=build_style_finder_dataset,
    ):
        self.model_name = model_name
        self.image_processor = image_processor or StyleFinderImageProcessor(
            image_size=STYLE_FINDER_IMAGE_SIZE
        )
        self.data = dataset_builder(self.image_processor)
        if self.data.empty:
            raise ValueError("The generated style finder dataset is empty.")

        self.llm_service_factory = llm_service_factory
        self.example_image_paths = ensure_style_finder_example_assets()

    def process_image(self, image, model_name: str | None = None) -> str:
        if image is None:
            return "Error: Please provide a fashion image."

        temporary_path = None
        image_path = image

        if not isinstance(image, (str, Path)):
            temporary_file = NamedTemporaryFile(delete=False, suffix=".png")
            temporary_path = temporary_file.name
            temporary_file.close()
            image.save(temporary_path)
            image_path = temporary_path

        try:
            user_encoding = self.image_processor.encode_image(image_path, is_url=False)
            if user_encoding["vector"] is None:
                return "Error: Unable to process the image. Please try another image."

            closest_row, similarity_score = self.image_processor.find_closest_match(
                user_encoding["vector"],
                self.data,
            )
            if closest_row is None:
                return "Error: Unable to find a match. Please try another image."

            all_items = get_all_items_for_image(closest_row["Image Key"], self.data)
            if all_items.empty:
                return "Error: No items found for the matched image."

            llm_service = self.llm_service_factory(model_name or self.model_name)
            bot_response = llm_service.generate_fashion_response(
                user_image_base64=user_encoding["base64"],
                matched_row=closest_row,
                all_items=all_items,
                similarity_score=similarity_score,
                threshold=STYLE_FINDER_SIMILARITY_THRESHOLD,
            )
            alternatives = build_alternatives_map(all_items, self.data)
            enhanced_response = format_alternatives_response(
                bot_response,
                alternatives,
                similarity_score,
                threshold=STYLE_FINDER_SIMILARITY_THRESHOLD,
            )
            return process_response(enhanced_response)
        finally:
            if temporary_path and os.path.exists(temporary_path):
                os.unlink(temporary_path)
