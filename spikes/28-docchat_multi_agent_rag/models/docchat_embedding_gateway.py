# --- DEPENDENCIAS ---
import hashlib
import math

from config.docchat_config import LOCAL_EMBEDDING_DIMENSION


class LocalHashEmbeddings:
    def __init__(self, dimension: int = LOCAL_EMBEDDING_DIMENSION):
        self.dimension = dimension

    def _embed_text(self, text: str) -> list[float]:
        vector = [0.0] * self.dimension
        for token in text.lower().split():
            digest = hashlib.sha256(token.encode("utf-8")).hexdigest()
            bucket = int(digest[:8], 16) % self.dimension
            sign = -1.0 if int(digest[8:10], 16) % 2 else 1.0
            vector[bucket] += sign

        norm = math.sqrt(sum(value * value for value in vector)) or 1.0
        return [value / norm for value in vector]

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self._embed_text(text) for text in texts]

    def embed_query(self, text: str) -> list[float]:
        return self._embed_text(text)


def build_docchat_embeddings() -> LocalHashEmbeddings:
    return LocalHashEmbeddings()