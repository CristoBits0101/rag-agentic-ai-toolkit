# --- DEPENDENCIAS ---
import json
from urllib.error import HTTPError
from urllib.error import URLError
from urllib.request import Request
from urllib.request import urlopen

from config.natural_language_sql_agent_config import OLLAMA_MODEL_CANDIDATES
from config.natural_language_sql_agent_config import OLLAMA_TAGS_URL

try:
    from langchain_ollama import ChatOllama
except Exception:
    ChatOllama = None


def list_installed_ollama_models(api_url: str = OLLAMA_TAGS_URL) -> list[str]:
    request = Request(api_url, headers={"Accept": "application/json"}, method="GET")

    try:
        with urlopen(request, timeout=30) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        raise RuntimeError(f"Ollama tags endpoint returned HTTP {exc.code}.") from exc
    except URLError as exc:
        raise RuntimeError("Ollama could not be reached. Verify ollama serve is running.") from exc
    except Exception as exc:
        raise RuntimeError("Ollama tags endpoint returned an invalid response.") from exc

    return [entry.get("name", "").strip() for entry in payload.get("models", []) if entry.get("name")]


def normalize_model_name(model_name: str) -> str:
    return model_name.strip().lower()


def select_best_available_ollama_model(
    installed_models: list[str] | None = None,
    preferred_models: tuple[str, ...] = OLLAMA_MODEL_CANDIDATES,
) -> str:
    if not installed_models:
        return preferred_models[0]

    normalized_installed = {normalize_model_name(name): name for name in installed_models}
    for preferred_model in preferred_models:
        preferred_name = normalize_model_name(preferred_model)
        if preferred_name in normalized_installed:
            return normalized_installed[preferred_name]

        preferred_base = preferred_name.split(":", maxsplit=1)[0]
        for installed_name in installed_models:
            installed_base = normalize_model_name(installed_name).split(":", maxsplit=1)[0]
            if installed_base == preferred_base:
                return installed_name

    return installed_models[0]


def build_natural_language_sql_ollama_chat_model(
    model_name: str | None = None,
    tags_loader=list_installed_ollama_models,
):
    if ChatOllama is None:
        raise RuntimeError(
            "LangChain Ollama is not available. Install langchain-ollama before running practica 23."
        )

    installed_models = tags_loader()
    selected_model = model_name or select_best_available_ollama_model(installed_models)
    return ChatOllama(
        model=selected_model,
        temperature=0,
        disable_streaming="tool_calling",
        validate_model_on_init=False,
    )
