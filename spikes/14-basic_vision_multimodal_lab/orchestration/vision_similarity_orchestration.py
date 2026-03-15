# --- DEPENDENCIAS ---
import numpy as np

from data.vision_sample_dataset import FASHION_CATALOG_ITEMS
from data.vision_sample_dataset import VISION_SAMPLE_RECORDS
from models.vision_demo_model import decode_sample_record

# --- SIMILARITY ---
VISION_VOCABULARY = (
    "fashion",
    "business",
    "casual",
    "formal",
    "navy",
    "white",
    "black",
    "olive",
    "beige",
    "blazer",
    "blouse",
    "trousers",
    "overshirt",
    "chinos",
    "dress",
    "silver",
)


def build_term_vector(terms: tuple[str, ...]) -> np.ndarray:
    normalized_terms = {term.lower() for term in terms}
    return np.array(
        [1.0 if token in normalized_terms else 0.0 for token in VISION_VOCABULARY],
        dtype=float,
    )


def build_catalog_dataset() -> list[dict]:
    dataset = []

    for item in FASHION_CATALOG_ITEMS:
        dataset.append(
            {
                "Item Name": item.item_name,
                "Price": item.price,
                "Link": item.link,
                "Embedding": build_term_vector(item.vector_terms),
            }
        )

    return dataset


def build_image_vector(encoded_image: str) -> np.ndarray:
    record = decode_sample_record(encoded_image)
    if not record:
        raise ValueError("Unsupported encoded image for similarity matching.")

    return build_term_vector(record.vector_terms)


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
