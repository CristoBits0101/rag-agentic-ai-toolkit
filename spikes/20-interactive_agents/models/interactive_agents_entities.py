# --- DEPENDENCIAS ---
from dataclasses import dataclass
from typing import Any

from langchain_core.messages import BaseMessage


@dataclass(frozen=True)
class ParsedToolCall:
    tool_name: str
    arguments: dict[str, Any]
    tool_call_id: str


@dataclass(frozen=True)
class InteractiveToolStep:
    tool_name: str
    arguments: dict[str, Any]
    result: dict[str, Any]


@dataclass(frozen=True)
class InteractiveToolRunResult:
    query: str
    final_answer: str
    tool_calls: list[ParsedToolCall]
    steps: list[InteractiveToolStep]
    messages: list[BaseMessage]
