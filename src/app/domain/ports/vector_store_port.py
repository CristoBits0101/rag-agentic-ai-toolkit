from typing import Protocol

from app.domain.models.retrieval import RetrievalDocument, RetrievalQuery


class VectorStorePort(Protocol):
    def upsert(self, docs: list[RetrievalDocument]) -> None:
        """Insert or update documents."""

    def search(self, query: RetrievalQuery) -> list[RetrievalDocument]:
        """Search similar documents."""
