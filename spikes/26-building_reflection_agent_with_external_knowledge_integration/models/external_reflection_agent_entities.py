# --- DEPENDENCIAS ---
from dataclasses import dataclass


@dataclass(frozen=True)
class ExternalReflectionAgentResult:
    question: str
    initial_answer: str
    revised_answers: tuple[str, ...]
    final_answer: str
    reflections: tuple[dict[str, str], ...]
    references: tuple[str, ...]
    search_queries: tuple[tuple[str, ...], ...]
    total_messages: int
    mermaid_graph: str