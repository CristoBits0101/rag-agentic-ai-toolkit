# --- DEPENDENCIAS ---
from dataclasses import dataclass
from typing import Any

from langchain_core.messages import BaseMessage


@dataclass(frozen=True)
class ToolCallingStep:
    tool_name: str
    arguments: dict[str, Any]
    result: dict[str, Any]


@dataclass(frozen=True)
class ToolCallingRunResult:
    query: str
    final_answer: str
    steps: list[ToolCallingStep]
    messages: list[BaseMessage]
