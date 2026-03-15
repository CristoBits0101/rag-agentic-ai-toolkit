# --- DEPENDENCIAS ---
import json
import os
from urllib.error import HTTPError
from urllib.error import URLError
from urllib.request import Request
from urllib.request import urlopen

from config.story_real_provider_config import MISTRAL_API_MODEL_NAME
from config.story_real_provider_config import MISTRAL_API_URL

# --- MODEL ---
def build_mistral_request_payload(
    prompt: str,
    model_name: str = MISTRAL_API_MODEL_NAME,
) -> dict:
    return {
        "model": model_name,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.4,
        "max_tokens": 768,
    }


def extract_mistral_text(response_payload: dict) -> str:
    choices = response_payload.get("choices", [])
    if not choices:
        raise RuntimeError("Mistral API returned no choices.")

    content = choices[0].get("message", {}).get("content", "")
    if isinstance(content, str):
        return content.strip()

    if isinstance(content, list):
        return " ".join(
            part.get("text", "").strip()
            for part in content
            if isinstance(part, dict) and part.get("text")
        ).strip()

    raise RuntimeError("Mistral API returned an unsupported content format.")


def generate_story_with_mistral_api(
    prompt: str,
    model_name: str = MISTRAL_API_MODEL_NAME,
) -> str:
    api_key = os.getenv("MISTRAL_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("MISTRAL_API_KEY is required for the Mistral API variant.")

    payload = build_mistral_request_payload(prompt, model_name=model_name)
    request = Request(
        MISTRAL_API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )

    try:
        with urlopen(request, timeout=90) as response:
            response_payload = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        raise RuntimeError(f"Mistral API returned HTTP {exc.code}.") from exc
    except URLError as exc:
        raise RuntimeError("Mistral API could not be reached.") from exc
    except Exception as exc:
        raise RuntimeError("Mistral API returned an invalid response.") from exc

    return extract_mistral_text(response_payload)
