# --- DEPENDENCIAS ---
from dataclasses import dataclass
from dataclasses import field
from typing import Any


@dataclass(slots=True)
class VoiceActionPlan:
    action: str
    parameters: dict[str, Any] = field(default_factory=dict)
    response: str = ""
    requires_confirmation: bool = False
    confirmation_prompt: str = ""
    planner_provider: str = "demo"
    planner_model: str = "rule_based"


@dataclass(slots=True)
class VoiceExecutionResult:
    success: bool
    message: str
    action: str
