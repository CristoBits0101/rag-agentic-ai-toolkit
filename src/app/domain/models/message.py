from dataclasses import dataclass, field


@dataclass(slots=True)
class Message:
    role: str
    content: str
    metadata: dict[str, str] = field(default_factory=dict)
