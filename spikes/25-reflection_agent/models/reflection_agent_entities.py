# --- DEPENDENCIAS ---
from dataclasses import dataclass


@dataclass(frozen=True)
class ReflectionAgentRunResult:
    request: str
    generated_posts: tuple[str, ...]
    critiques: tuple[str, ...]
    final_post: str
    total_messages: int
    mermaid_graph: str