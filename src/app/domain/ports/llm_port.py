from typing import Protocol


class LlmPort(Protocol):
    def complete(self, prompt: str, *, temperature: float = 0.0) -> str:
        """Generate a completion for a prompt."""
