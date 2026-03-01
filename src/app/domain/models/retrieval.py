from dataclasses import dataclass


@dataclass(slots=True)
class RetrievalQuery:
    query: str
    top_k: int = 5


@dataclass(slots=True)
class RetrievalDocument:
    doc_id: str
    content: str
    score: float | None = None
