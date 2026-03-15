from typing import Protocol


class SearchPort(Protocol):
    def search(self, query: str, *, limit: int = 5) -> list[str]:
        """Search data from a web or enterprise source."""
