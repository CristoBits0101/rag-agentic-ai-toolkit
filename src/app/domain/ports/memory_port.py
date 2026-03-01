from typing import Protocol

from app.domain.models.message import Message


class MemoryPort(Protocol):
    def append(self, conversation_id: str, message: Message) -> None:
        """Append a message into a conversation memory store."""

    def load(self, conversation_id: str) -> list[Message]:
        """Load a conversation history."""
