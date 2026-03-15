from dataclasses import dataclass, field


@dataclass(slots=True)
class AgentRun:
    run_id: str
    status: str = "pending"
    steps: list[str] = field(default_factory=list)
    output: str | None = None
