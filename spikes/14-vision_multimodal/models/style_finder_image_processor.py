# --- DEPENDENCIAS ---
import base64
from io import BytesIO
from pathlib import Path
from urllib.request import urlopen

import numpy as np
from PIL import Image

try:
    import torch
    from torchvision.models import ResNet50_Weights
    from torchvision.models import resnet50
except ImportError:
    torch = None
    ResNet50_Weights = None
    resnet50 = None


def cosine_similarity(left: np.ndarray, right: np.ndarray) -> float:
    denominator = np.linalg.norm(left) * np.linalg.norm(right)
    if denominator == 0:
        return 0.0

    return float(np.dot(left, right) / denominator)


class StyleFinderImageProcessor:
    def __init__(self, image_size=(128, 128), embedding_backend="auto"):
        self.image_size = image_size
        self.embedding_backend = self._resolve_backend(embedding_backend)
        self.device = None
        self.model = None
        self.preprocess = None

        if self.embedding_backend == "resnet50":
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            weights = ResNet50_Weights.DEFAULT
            self.model = resnet50(weights=weights).to(self.device)
            self.model.fc = torch.nn.Identity()
            self.model.eval()
            self.preprocess = weights.transforms()

    def _resolve_backend(self, embedding_backend: str) -> str:
        if embedding_backend == "auto":
            if torch is not None and resnet50 is not None and ResNet50_Weights is not None:
                return "resnet50"

            return "histogram"

        if embedding_backend == "resnet50":
            if torch is None or resnet50 is None or ResNet50_Weights is None:
                raise RuntimeError("ResNet50 requires torch and torchvision.")

            return "resnet50"

        if embedding_backend == "histogram":
            return "histogram"

        raise ValueError(f"Unsupported embedding backend: {embedding_backend}")

    def load_image(self, image_input, is_url=True) -> Image.Image:
        if is_url:
            with urlopen(image_input, timeout=30) as response:
                return Image.open(BytesIO(response.read())).convert("RGB")

        return Image.open(image_input).convert("RGB")

    def encode_image(self, image_input, is_url=True):
        try:
            image = self.load_image(image_input, is_url=is_url)
            buffered = BytesIO()
            image.save(buffered, format="JPEG")
            base64_string = base64.b64encode(buffered.getvalue()).decode("utf-8")
            feature_vector = self.extract_feature_vector(image)
            return {"base64": base64_string, "vector": feature_vector}
        except Exception:
            return {"base64": None, "vector": None}

    def extract_feature_vector(self, image: Image.Image) -> np.ndarray:
        if self.embedding_backend == "resnet50":
            input_tensor = self.preprocess(image).unsqueeze(0).to(self.device)
            with torch.no_grad():
                features = self.model(input_tensor)

            return features.cpu().numpy().flatten()

        resized = image.resize(self.image_size).convert("RGB")
        image_array = np.asarray(resized, dtype=np.float32) / 255.0
        height, width, _ = image_array.shape
        upper_half = image_array[: height // 2]
        lower_half = image_array[height // 2 :]
        center_patch = image_array[height // 4 : 3 * height // 4, width // 4 : 3 * width // 4]
        horizontal_edges = np.abs(np.diff(image_array, axis=1)).mean(axis=(0, 1))
        vertical_edges = np.abs(np.diff(image_array, axis=0)).mean(axis=(0, 1))
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
                horizontal_edges,
                vertical_edges,
                np.asarray(histogram, dtype=np.float32),
            ]
        )

    def find_closest_match(self, user_vector, dataset):
        try:
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
        except Exception:
            return None, None

    def build_embedding_for_path(self, image_path: str | Path) -> np.ndarray:
        image = self.load_image(image_path, is_url=False)
        return self.extract_feature_vector(image)
