# --- DEPENDENCIAS ---
from dataclasses import dataclass
from typing import Any

from langchain_core.messages import BaseMessage


@dataclass(frozen=True)
class DataWizardStep:
    tool_name: str
    arguments: dict[str, Any]
    result: dict[str, Any]


@dataclass(frozen=True)
class DataWizardRunResult:
    query: str
    final_answer: str
    steps: list[DataWizardStep]
    messages: list[BaseMessage]
