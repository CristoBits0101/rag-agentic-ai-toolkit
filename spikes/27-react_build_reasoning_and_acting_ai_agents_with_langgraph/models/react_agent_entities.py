# --- DEPENDENCIAS ---
from dataclasses import dataclass
from typing import Any

from langchain_core.messages import BaseMessage


@dataclass(frozen=True)
class ReactToolStep:
    tool_name: str
    arguments: dict[str, Any]
    result: Any


@dataclass(frozen=True)
class ReactAgentRunResult:
    query: str
    final_answer: str
    steps: tuple[ReactToolStep, ...]
    messages: tuple[BaseMessage, ...]
    mermaid_graph: str