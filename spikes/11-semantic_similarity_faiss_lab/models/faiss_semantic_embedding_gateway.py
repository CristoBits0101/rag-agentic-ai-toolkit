# --- DEPENDENCIAS ---
# 1. Numpy: Para construir vectores numericos compatibles con FAISS.
# 2. Regex: Para tokenizar texto de forma simple.
import re

import numpy as np

# --- EMBEDDINGS ---
SEMANTIC_GROUPS = {
    "motorcycles_core": {
        "bike",
        "brake",
        "engine",
        "helmet",
        "motorcycle",
        "motorcycles",
        "rider",
        "riders",
        "road",
    },
    "motorcycles_safety": {
        "boots",
        "gear",
        "gloves",
        "jacket",
        "padding",
        "protection",
        "safety",
        "touring",
    },
    "space_core": {
        "astronaut",
        "launch",
        "mars",
        "mission",
        "moon",
        "nasa",
        "orbit",
        "orbital",
        "rocket",
        "space",
    },
    "space_science": {
        "crater",
        "guidance",
        "lunar",
        "satellite",
        "shuttle",
        "simulator",
        "station",
        "telescope",
        "transit",
    },
    "graphics_core": {
        "animation",
        "design",
        "graphics",
        "gpu",
        "image",
        "pixels",
        "render",
        "rendering",
        "shader",
        "texture",
    },
    "graphics_scene": {
        "driver",
        "engine",
        "lighting",
        "memory",
        "model",
        "output",
        "scene",
        "streaming",
        "video",
    },
    "medicine_core": {
        "clinic",
        "disease",
        "doctor",
        "doctors",
        "medical",
        "medicine",
        "patient",
        "therapy",
        "treatment",
    },
    "medicine_care": {
        "diagnostic",
        "exercise",
        "fatigue",
        "health",
        "infection",
        "medication",
        "monitoring",
        "pain",
        "symptoms",
    },
}


def tokenize_text(text: str) -> list[str]:
    # Extrae tokens alfabeticos en minusculas.
    return re.findall(r"[a-z]+", text.lower())


def build_semantic_vector(text: str) -> np.ndarray:
    # Cuenta señales semanticas del dominio en un vector float32.
    tokens = tokenize_text(text)
    vector = np.array(
        [
            float(sum(token in keywords for token in tokens))
            for keywords in SEMANTIC_GROUPS.values()
        ]
        + [1.0],
        dtype="float32",
    )
    return vector


def embed_texts(texts: list[str]) -> np.ndarray:
    # Apila embeddings de varios textos en una matriz FAISS.
    return np.vstack([build_semantic_vector(text) for text in texts]).astype("float32")
