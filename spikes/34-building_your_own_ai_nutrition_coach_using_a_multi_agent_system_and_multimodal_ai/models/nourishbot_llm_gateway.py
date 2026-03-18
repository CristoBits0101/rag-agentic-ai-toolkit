# --- DEPENDENCIAS ---
import json
from urllib.error import HTTPError
from urllib.error import URLError
from urllib.request import Request
from urllib.request import urlopen

from config.nourishbot_config import DEFAULT_TEXT_MODEL
from config.nourishbot_config import DEFAULT_VISION_MODEL
from config.nourishbot_config import VISION_API_URL
from langchain_ollama import ChatOllama


def build_text_model(model_name: str = DEFAULT_TEXT_MODEL):
    return ChatOllama(model=model_name, temperature=0)


def _build_vision_payload(model_name: str, prompt: str, encoded_image: str) -> dict:
    return {
        "model": model_name,
        "stream": False,
        "messages": [
            {
                "role": "user",
                "content": prompt,
                "images": [encoded_image],
            }
        ],
    }


def generate_vision_notes(encoded_image: str, prompt: str, model_name: str = DEFAULT_VISION_MODEL) -> str:
    payload = _build_vision_payload(model_name=model_name, prompt=prompt, encoded_image=encoded_image)
    request = Request(
        VISION_API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=120) as response:
            response_payload = json.loads(response.read().decode("utf-8"))
        content = response_payload.get("message", {}).get("content", "").strip()
        if not content:
            raise RuntimeError("Empty response from vision model.")
        return content
    except HTTPError as exc:
        raise RuntimeError(f"Vision API returned HTTP {exc.code}.") from exc
    except URLError as exc:
        raise RuntimeError("Vision API could not be reached.") from exc
    except Exception as exc:
        raise RuntimeError("Vision API request failed.") from exc