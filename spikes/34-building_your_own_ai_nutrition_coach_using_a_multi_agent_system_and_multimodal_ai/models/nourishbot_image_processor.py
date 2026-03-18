# --- DEPENDENCIAS ---
import base64
from io import BytesIO
from pathlib import Path

import numpy as np
from PIL import Image


def cosine_similarity(left: np.ndarray, right: np.ndarray) -> float:
    denominator = np.linalg.norm(left) * np.linalg.norm(right)
    if denominator == 0:
        return 0.0
    return float(np.dot(left, right) / denominator)


class NourishBotImageProcessor:
    def __init__(self, image_size=(128, 128)):
        self.image_size = image_size

    def load_image(self, image_input: str | Path) -> Image.Image:
        return Image.open(image_input).convert("RGB")

    def extract_feature_vector(self, image: Image.Image) -> np.ndarray:
        resized = image.resize(self.image_size).convert("RGB")
        image_array = np.asarray(resized, dtype=np.float32) / 255.0
        height, width, _ = image_array.shape
        upper_half = image_array[: height // 2]
        lower_half = image_array[height // 2 :]
        center_patch = image_array[height // 4 : 3 * height // 4, width // 4 : 3 * width // 4]
        histogram = []
        for channel in range(3):
            counts, _ = np.histogram(image_array[:, :, channel], bins=4, range=(0.0, 1.0))
            histogram.extend(counts.astype(np.float32) / image_array[:, :, channel].size)

        return np.concatenate(
            [
                image_array.mean(axis=(0, 1)),
                image_array.std(axis=(0, 1)),
                upper_half.mean(axis=(0, 1)),
                lower_half.mean(axis=(0, 1)),
                center_patch.mean(axis=(0, 1)),
                np.asarray(histogram, dtype=np.float32),
            ]
        )

    def encode_image(self, image_input: str | Path) -> dict[str, object]:
        image = self.load_image(image_input)
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        encoded = base64.b64encode(buffered.getvalue()).decode("utf-8")
        return {"base64": encoded, "vector": self.extract_feature_vector(image)}

    def find_closest_match(self, user_vector: np.ndarray, dataset):
        best_index = None
        best_score = -1.0
        for index, row in dataset.iterrows():
            score = cosine_similarity(user_vector, row["Embedding"])
            if score > best_score:
                best_score = score
                best_index = index
        if best_index is None:
            return None, None
        return dataset.loc[best_index], best_score

    def build_embedding_for_path(self, image_path: str | Path) -> np.ndarray:
        return self.extract_feature_vector(self.load_image(image_path))