# --- DEPENDENCIAS ---
import os
from pathlib import Path
from tempfile import NamedTemporaryFile

from flask import Flask
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from config.nutrition_coach_config import NUTRITION_COACH_DEFAULT_MODEL
from config.nutrition_coach_config import NUTRITION_COACH_DEFAULT_QUERY
from config.nutrition_coach_config import NUTRITION_COACH_HOST
from config.nutrition_coach_config import NUTRITION_COACH_IMAGE_SIZE
from config.nutrition_coach_config import NUTRITION_COACH_PORT
from config.nutrition_coach_config import NUTRITION_COACH_SECRET_KEY
from config.nutrition_coach_config import NUTRITION_COACH_STATIC_DIR
from config.nutrition_coach_config import NUTRITION_COACH_TEMPLATES_DIR
from models.nutrition_coach_image_processor import NutritionCoachImageProcessor
from models.nutrition_coach_llm_service import NutritionCoachVisionService
from orchestration.nutrition_coach_asset_orchestration import ensure_nutrition_coach_example_assets
from orchestration.nutrition_coach_dataset_orchestration import build_nutrition_coach_dataset
from orchestration.nutrition_coach_helpers import format_response
from orchestration.nutrition_coach_helpers import get_all_items_for_image


def create_nutrition_coach_app(
    model_name: str = NUTRITION_COACH_DEFAULT_MODEL,
    image_processor=None,
    llm_service_factory=NutritionCoachVisionService,
    dataset_builder=build_nutrition_coach_dataset,
):
    image_processor = image_processor or NutritionCoachImageProcessor(
        image_size=NUTRITION_COACH_IMAGE_SIZE
    )
    dataset = dataset_builder(image_processor)
    example_image_paths = ensure_nutrition_coach_example_assets()

    app = Flask(
        __name__,
        template_folder=str(NUTRITION_COACH_TEMPLATES_DIR),
        static_folder=str(NUTRITION_COACH_STATIC_DIR),
    )
    app.secret_key = NUTRITION_COACH_SECRET_KEY
    app.config["MODEL_NAME"] = model_name
    app.config["DATASET"] = dataset
    app.config["IMAGE_PROCESSOR"] = image_processor
    app.config["LLM_SERVICE_FACTORY"] = llm_service_factory
    app.config["EXAMPLE_IMAGE_PATHS"] = example_image_paths

    @app.route("/", methods=["GET", "POST"])
    def index():
        example_images = [
            {
                "name": image_key.replace("_", " ").title(),
                "file_name": path.name,
            }
            for image_key, path in app.config["EXAMPLE_IMAGE_PATHS"].items()
        ]
        example_images.sort(key=lambda item: item["name"])

        if request.method == "POST":
            user_query = request.form.get("user_query", NUTRITION_COACH_DEFAULT_QUERY)
            uploaded_file = request.files.get("file")

            if not uploaded_file or not uploaded_file.filename:
                flash("Please upload an image file.", "danger")
                return redirect(url_for("index"))

            temporary_file = NamedTemporaryFile(delete=False, suffix=".png")
            temporary_path = temporary_file.name
            temporary_file.close()
            uploaded_file.save(temporary_path)

            try:
                user_encoding = app.config["IMAGE_PROCESSOR"].encode_image(
                    temporary_path,
                    is_url=False,
                )
                if user_encoding["vector"] is None:
                    flash("Error processing the image. Please try again.", "danger")
                    return redirect(url_for("index"))

                closest_row, _ = app.config["IMAGE_PROCESSOR"].find_closest_match(
                    user_encoding["vector"],
                    app.config["DATASET"],
                )
                if closest_row is None:
                    flash("Unable to find a nutrition match for that image.", "danger")
                    return redirect(url_for("index"))

                related_items = get_all_items_for_image(
                    closest_row["Image Key"],
                    app.config["DATASET"],
                )
                if related_items.empty:
                    flash("No nutrition records were found for the matched meal.", "danger")
                    return redirect(url_for("index"))

                llm_service = app.config["LLM_SERVICE_FACTORY"](app.config["MODEL_NAME"])
                response_text = llm_service.generate_nutrition_response(
                    user_image_base64=user_encoding["base64"],
                    related_items=related_items,
                    user_query=user_query,
                )
                return render_template(
                    "index.html",
                    response=format_response(response_text),
                    user_query=user_query,
                    current_model=app.config["MODEL_NAME"],
                    example_images=example_images,
                )
            finally:
                if os.path.exists(temporary_path):
                    os.unlink(temporary_path)

        return render_template(
            "index.html",
            response=None,
            user_query=NUTRITION_COACH_DEFAULT_QUERY,
            current_model=app.config["MODEL_NAME"],
            example_images=example_images,
        )

    return app


def launch_nutrition_coach_app(model_name: str = NUTRITION_COACH_DEFAULT_MODEL):
    app = create_nutrition_coach_app(model_name=model_name)
    app.run(debug=True, host=NUTRITION_COACH_HOST, port=NUTRITION_COACH_PORT)
