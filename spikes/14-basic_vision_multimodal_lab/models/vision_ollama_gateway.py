# --- DEPENDENCIAS ---
import base64
import json
from pathlib import Path
from urllib.error import HTTPError
from urllib.error import URLError
from urllib.request import Request
from urllib.request import urlopen

from config.vision_real_provider_config import OLLAMA_VISION_API_URL

# --- MODEL ---
def encode_real_image_file(image_path: str | Path) -> str:
    path = Path(image_path)
    return base64.b64encode(path.read_bytes()).decode("utf-8")


def build_ollama_vision_payload(
    model_name: str,
    prompt: str,
    image_path: str | Path,
) -> dict:
    return {
        "model": model_name,
        "stream": False,
        "messages": [
            {
                "role": "user",
                "content": prompt,
                "images": [encode_real_image_file(image_path)],
            }
        ],
    }


def extract_ollama_vision_text(response_payload: dict) -> str:
    return response_payload.get("message", {}).get("content", "").strip()


def send_ollama_vision_request(
    payload: dict,
    api_url: str = OLLAMA_VISION_API_URL,
) -> dict:
    request = Request(
        api_url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )

    try:
        with urlopen(request, timeout=120) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        raise RuntimeError(f"Ollama vision API returned HTTP {exc.code}.") from exc
    except URLError as exc:
        raise RuntimeError(
            "Ollama vision API could not be reached. Verify ollama serve is running."
        ) from exc
    except Exception as exc:
        raise RuntimeError("Ollama vision API returned an invalid response.") from exc


def generate_ollama_vision_response(
    model_name: str,
    prompt: str,
    image_path: str | Path,
    request_sender=send_ollama_vision_request,
) -> str:
    payload = build_ollama_vision_payload(model_name, prompt, image_path)
    response_payload = request_sender(payload)
    content = extract_ollama_vision_text(response_payload)
    if not content:
        raise RuntimeError(
            f"Ollama returned an empty response for model {model_name}. Verify the model is installed."
        )

    return content
