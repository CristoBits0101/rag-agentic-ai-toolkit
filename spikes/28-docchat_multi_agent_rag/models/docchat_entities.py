# --- DEPENDENCIAS ---
from dataclasses import dataclass


@dataclass(frozen=True)
class WorkflowResult:
    question: str
    relevance_label: str
    draft_answer: str
    final_answer: str
    verification_report: str
    context_used: str
    loop_count: int
    sources: tuple[str, ...]


@dataclass(frozen=True)
class ExampleSelectionResult:
    question: str
    file_paths: tuple[str, ...]