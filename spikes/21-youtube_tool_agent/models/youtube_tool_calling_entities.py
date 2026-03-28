# --- DEPENDENCIAS ---
from dataclasses import dataclass
from typing import Any

from langchain_core.messages import BaseMessage


@dataclass(frozen=True)
class YouTubeParsedToolCall:
    tool_name: str
    arguments: dict[str, Any]
    tool_call_id: str


@dataclass(frozen=True)
class YouTubeToolStep:
    tool_name: str
    arguments: dict[str, Any]
    result: Any


@dataclass(frozen=True)
class YouTubeToolRunResult:
    query: str
    final_answer: str
    tool_calls: list[YouTubeParsedToolCall]
    steps: list[YouTubeToolStep]
    messages: list[BaseMessage]
