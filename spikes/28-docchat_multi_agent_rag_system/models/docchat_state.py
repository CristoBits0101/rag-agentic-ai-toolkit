# --- DEPENDENCIAS ---
from typing import Any
from typing import TypedDict


class AgentState(TypedDict, total=False):
    question: str
    retriever: Any
    retrieved_docs: list[Any]
    relevance_label: str
    draft_answer: str
    final_answer: str
    verification_report: str
    context_used: str
    loop_count: int
    sources: list[str]