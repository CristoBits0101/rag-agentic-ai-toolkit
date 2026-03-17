# --- DEPENDENCIAS ---
import base64
from io import BytesIO

import numpy as np
from PIL import Image

from data.style_finder_fashion_dataset import STYLE_FINDER_OUTFITS
from models.style_finder_image_processor import StyleFinderImageProcessor
from orchestration.style_finder_asset_orchestration import ensure_style_finder_example_assets

# --- SIMILARITY ---
def build_catalog_dataset() -> list[dict]:
    image_processor = StyleFinderImageProcessor()
    image_paths = ensure_style_finder_example_assets()
    dataset = []

    for outfit in STYLE_FINDER_OUTFITS:
        primary_item = outfit["items"][0]
        dataset.append(
            {
                "Item Name": primary_item["Item Name"],
                "Look Title": outfit["title"],
                "Price": primary_item["Price"],
                "Link": primary_item["Link"],
                "Embedding": image_processor.build_embedding_for_path(
                    image_paths[outfit["image_key"]]
                ),
            }
        )

    return dataset


def build_image_vector(encoded_image: str) -> np.ndarray:
    image_bytes = base64.b64decode(encoded_image)
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    image_processor = StyleFinderImageProcessor()
    return image_processor.extract_feature_vector(image)


def cosine_similarity_score(left: np.ndarray, right: np.ndarray) -> float:
    denominator = np.linalg.norm(left) * np.linalg.norm(right)
    if denominator == 0:
        return 0.0

    return float(np.dot(left, right) / denominator)


def find_closest_match(user_vector: np.ndarray, dataset: list[dict]):
    best_row = None
    best_score = -1.0

    for row in dataset:
        score = cosine_similarity_score(user_vector, row["Embedding"])
        if score > best_score:
            best_score = score
            best_row = row

    return best_row, best_score
