from typing import Any


class HttpClient:
    def get_json(self, url: str, timeout: float = 10.0) -> dict[str, Any]:
        try:
            import httpx
        except ImportError as exc:
            raise RuntimeError("Missing dependency: install httpx to use HttpClient.") from exc

        response = httpx.get(url, timeout=timeout)
        response.raise_for_status()
        return response.json()
