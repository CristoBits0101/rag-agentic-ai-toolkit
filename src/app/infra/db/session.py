from typing import Any


class DBSession:
    def __enter__(self) -> "DBSession":
        return self

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        return None
