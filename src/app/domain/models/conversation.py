from dataclasses import dataclass, field

from app.domain.models.message import Message


@dataclass(slots=True)
class Conversation:
    conversation_id: str
    user_id: str | None = None
    messages: list[Message] = field(default_factory=list)
