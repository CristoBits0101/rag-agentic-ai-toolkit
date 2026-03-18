# --- DEPENDENCIAS ---
from dataclasses import dataclass


@dataclass(frozen=True)
class AuthWorkflowResult:
    username: str
    is_authenticated: bool
    output: str
    attempts: int


@dataclass(frozen=True)
class QAWorkflowResult:
    question: str
    context: str | None
    answer: str
    valid: bool
    error: str | None


@dataclass(frozen=True)
class CounterWorkflowResult:
    n: int
    letter: str