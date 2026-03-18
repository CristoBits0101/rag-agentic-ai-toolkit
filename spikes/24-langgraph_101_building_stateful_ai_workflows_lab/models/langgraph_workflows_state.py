# --- DEPENDENCIAS ---
from typing import TypedDict


class AuthState(TypedDict, total=False):
    username: str
    password: str
    is_authenticated: bool
    output: str
    credential_attempts: list[dict[str, str]]
    attempt_index: int
    attempts: int
    max_attempts: int


class QAState(TypedDict, total=False):
    question: str
    valid: bool
    error: str
    context: str | None
    answer: str


class ChainState(TypedDict):
    n: int
    letter: str