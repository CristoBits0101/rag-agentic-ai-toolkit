# --- DEPENDENCIAS ---
from dataclasses import dataclass


@dataclass(frozen=True)
class WorkflowPatternResult:
    pattern_name: str
    summary: str
    details: dict