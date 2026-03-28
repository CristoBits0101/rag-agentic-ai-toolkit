# --- DEPENDENCIAS ---
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class VisualizationAgentResult:
    query: str
    output: str
    generated_code: str
    artifact_path: Path | None
    artifact_exists: bool
