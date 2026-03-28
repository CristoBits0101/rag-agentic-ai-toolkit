# --- DEPENDENCIAS ---
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPIKE = ROOT / "spikes" / "14-vision_multimodal"

if str(SPIKE) not in sys.path:
    sys.path.insert(0, str(SPIKE))

from config.style_finder_fashion_config import STYLE_FINDER_SUPPORTED_MODELS
from models.style_finder_image_processor import StyleFinderImageProcessor
from models.style_finder_llm_service import StyleFinderVisionService
from orchestration.style_finder_app_orchestration import StyleFinderApp
from orchestration.style_finder_asset_orchestration import ensure_style_finder_example_assets
from orchestration.style_finder_dataset_orchestration import build_style_finder_dataset
from orchestration.style_finder_helpers import build_alternatives_map
from orchestration.style_finder_helpers import format_alternatives_response
from orchestration.style_finder_helpers import get_all_items_for_image
from ui.style_finder_ui import build_style_finder_interface


class FakeStyleFinderService:
    def __init__(self, model_name):
        self.model_name = model_name

    def generate_fashion_response(
        self,
        user_image_base64,
        matched_row,
        all_items,
        similarity_score,
        threshold=0.8,
    ):
        return (
            f"Matched look: {matched_row['Look Title']}.\n\n"
            "ITEM DETAILS:\n"
            f"- {all_items.iloc[0]['Item Name']} (${all_items.iloc[0]['Price']:.2f})"
        )


def test_style_finder_example_assets_are_created():
    image_paths = ensure_style_finder_example_assets()

    assert len(image_paths) == 4
    assert all(path.exists() for path in image_paths.values())


def test_style_finder_dataset_contains_embeddings():
    image_processor = StyleFinderImageProcessor()
    dataset = build_style_finder_dataset(image_processor)

    assert len(dataset) == 12
    assert "Embedding" in dataset.columns
    assert dataset.iloc[0]["Embedding"].size > 0


def test_get_all_items_for_image_returns_grouped_rows():
    image_processor = StyleFinderImageProcessor()
    dataset = build_style_finder_dataset(image_processor)
    image_key = dataset.iloc[0]["Image Key"]
    related_items = get_all_items_for_image(image_key, dataset)

    assert len(related_items) == 3
    assert all(related_items["Image Key"] == image_key)


def test_build_alternatives_map_returns_cross_look_options():
    image_processor = StyleFinderImageProcessor()
    dataset = build_style_finder_dataset(image_processor)
    related_items = get_all_items_for_image("sparkle_blazer_night", dataset)
    alternatives = build_alternatives_map(related_items, dataset)

    assert "Midnight sequin blazer" in alternatives
    assert alternatives["Midnight sequin blazer"]
    assert any("Sand blazer" in item["title"] for item in alternatives["Midnight sequin blazer"])


def test_format_alternatives_response_appends_markdown_section():
    formatted = format_alternatives_response(
        "",
        {
            "Midnight sequin blazer": [
                {
                    "title": "Sand blazer",
                    "price": "$210.00",
                    "source": "Style Finder Archive",
                    "link": "https://style-finder.local/sand-blazer",
                }
            ]
        },
        similarity_score=0.9,
    )

    assert "## Similar Items Found" in formatted
    assert "Sand blazer" in formatted


def test_style_finder_service_returns_explicit_error_when_response_is_short():
    image_processor = StyleFinderImageProcessor()
    dataset = build_style_finder_dataset(image_processor)
    matched_row = dataset.iloc[0]
    all_items = get_all_items_for_image(matched_row["Image Key"], dataset)
    service = StyleFinderVisionService(
        STYLE_FINDER_SUPPORTED_MODELS[0],
        response_generator=lambda model_name, prompt, encoded_image: "Too short.",
    )

    response = service.generate_fashion_response(
        user_image_base64="encoded-image",
        matched_row=matched_row,
        all_items=all_items,
        similarity_score=0.95,
    )

    assert "Error generating response" in response
    assert "ITEM DETAILS:" in response


def test_style_finder_app_process_image_returns_markdown_analysis():
    app = StyleFinderApp(llm_service_factory=FakeStyleFinderService)
    first_example_path = str(next(iter(app.example_image_paths.values())))
    response = app.process_image(first_example_path, STYLE_FINDER_SUPPORTED_MODELS[0])

    assert response.startswith("# Fashion Analysis")
    assert "## Similar Items Found" in response
    assert "Buy it here" in response


def test_style_finder_interface_builds_blocks():
    app = StyleFinderApp(llm_service_factory=FakeStyleFinderService)
    interface = build_style_finder_interface(app)

    assert interface is not None


def test_style_finder_variant_subfolders_exist():
    assert (SPIKE / "style_finder_fashion_rag_app" / "main.py").exists()
    assert (SPIKE / "style_finder_llama3_2_vision_app" / "main.py").exists()
    assert (SPIKE / "style_finder_llava_app" / "main.py").exists()
    assert (SPIKE / "style_finder_qwen2_5vl_app" / "main.py").exists()
