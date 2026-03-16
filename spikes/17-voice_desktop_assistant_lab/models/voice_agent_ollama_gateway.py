# --- DEPENDENCIAS ---
import json
import unicodedata
from urllib.error import HTTPError
from urllib.error import URLError
from urllib.request import Request
from urllib.request import urlopen

from config.voice_desktop_config import DEFAULT_CONFIRMATION_PROMPT
from config.voice_desktop_config import OLLAMA_API_URL
from config.voice_desktop_config import OLLAMA_MODEL_CANDIDATES
from config.voice_desktop_config import OLLAMA_TAGS_URL
from config.voice_desktop_config import SENSITIVE_ACTIONS
from data.voice_command_catalog import ALLOWED_ACTIONS
from data.voice_command_catalog import ALLOWED_APPLICATIONS
from data.voice_command_catalog import APPLICATION_ALIASES
from data.voice_command_catalog import CLOSEABLE_APPLICATION_PROCESSES
from models.voice_desktop_entities import VoiceActionPlan


ACTION_ALIASES = {
    "close_app": "close_application",
    "delete_path": "trash_path",
    "open_app": "open_application",
}


def normalize_text(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text or "")
    return normalized.encode("ascii", "ignore").decode("ascii").lower().strip()


def normalize_model_name(model_name: str) -> str:
    return model_name.strip().lower()


def normalize_action_name(action_name: object) -> str:
    normalized = normalize_text(str(action_name)).replace(" ", "_")
    return ACTION_ALIASES.get(normalized, normalized)


def normalize_application_name(
    application_name: object,
    allowed_applications: dict[str, list[str]],
) -> str:
    normalized = normalize_text(str(application_name))
    if not normalized:
        raise RuntimeError("Ollama returned an empty application name.")

    if normalized in allowed_applications:
        return normalized

    if normalized in APPLICATION_ALIASES:
        resolved_name = APPLICATION_ALIASES[normalized]
        if resolved_name in allowed_applications:
            return resolved_name

    for alias, resolved_name in APPLICATION_ALIASES.items():
        if alias in normalized and resolved_name in allowed_applications:
            return resolved_name

    raise RuntimeError(f"Ollama returned an unsupported application name: {application_name}.")


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


def build_ollama_command_payload(model_name: str, transcript: str) -> dict:
    allowed_apps = ", ".join(sorted(ALLOWED_APPLICATIONS))
    closeable_apps = ", ".join(sorted(CLOSEABLE_APPLICATION_PROCESSES))
    allowed_actions = ", ".join(ALLOWED_ACTIONS)

    system_message = (
        "Eres un planificador de comandos de escritorio seguro. "
        "Devuelve solo JSON valido sin markdown. "
        "Las acciones permitidas son: "
        f"{allowed_actions}. "
        "Usa close_application solo para aplicaciones permitidas y requiere confirmacion. "
        "Usa trash_path solo para enviar a la papelera. "
        "Pon requires_confirmation en true para acciones destructivas. "
        f"Las aplicaciones permitidas son: {allowed_apps}. "
        f"Las aplicaciones permitidas para cerrar son: {closeable_apps}."
    )

    user_message = (
        "Transcripcion del usuario:\n"
        f"{transcript}\n\n"
        "Responde con este esquema JSON exacto:\n"
        '{'
        '"action":"answer|close_application|no_op|open_application|open_url|press_hotkey|trash_path|type_text",'
        '"parameters":{},'
        '"response":"mensaje breve en espanol",'
        '"requires_confirmation":false,'
        '"confirmation_prompt":"mensaje breve o vacio"'
        '}'
    )

    return {
        "model": model_name,
        "stream": False,
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ],
        "options": {
            "temperature": 0,
        },
    }


def send_ollama_command_request(
    payload: dict,
    api_url: str = OLLAMA_API_URL,
) -> dict:
    request = Request(
        api_url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urlopen(request, timeout=120) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        raise RuntimeError(f"Ollama command endpoint returned HTTP {exc.code}.") from exc
    except URLError as exc:
        raise RuntimeError("Ollama command endpoint could not be reached.") from exc
    except Exception as exc:
        raise RuntimeError("Ollama command endpoint returned an invalid response.") from exc


def extract_ollama_text(response_payload: dict) -> str:
    return response_payload.get("message", {}).get("content", "").strip()


def extract_plan_payload(response_text: str) -> dict:
    cleaned = response_text.strip()
    start_index = cleaned.find("{")
    end_index = cleaned.rfind("}")
    if start_index == -1 or end_index == -1:
        raise RuntimeError("Ollama did not return a JSON plan.")

    return json.loads(cleaned[start_index : end_index + 1])


def normalize_plan_payload(
    payload: dict,
    planner_model: str,
) -> VoiceActionPlan:
    action = normalize_action_name(payload.get("action", "answer"))
    if action not in ALLOWED_ACTIONS:
        raise RuntimeError(f"Ollama returned an unsupported action: {action}.")

    parameters = payload.get("parameters") if isinstance(payload.get("parameters"), dict) else {}
    response = str(payload.get("response", "")).strip() or "Orden procesada."
    requires_confirmation = bool(payload.get("requires_confirmation", False))
    confirmation_prompt = str(payload.get("confirmation_prompt", "")).strip()

    if action == "open_application":
        parameters = {
            **parameters,
            "application": normalize_application_name(
                parameters.get("application"),
                ALLOWED_APPLICATIONS,
            ),
        }

    if action == "close_application":
        parameters = {
            **parameters,
            "application": normalize_application_name(
                parameters.get("application"),
                CLOSEABLE_APPLICATION_PROCESSES,
            ),
        }

    if action in SENSITIVE_ACTIONS:
        requires_confirmation = True
        confirmation_prompt = confirmation_prompt or DEFAULT_CONFIRMATION_PROMPT

    return VoiceActionPlan(
        action=action,
        parameters=parameters,
        response=response,
        requires_confirmation=requires_confirmation,
        confirmation_prompt=confirmation_prompt,
        planner_provider="ollama",
        planner_model=planner_model,
    )


def plan_voice_command_with_ollama(
    transcript: str,
    model_name: str | None = None,
    request_sender=send_ollama_command_request,
    tags_loader=list_installed_ollama_models,
) -> VoiceActionPlan:
    installed_models = tags_loader()
    selected_model = model_name or select_best_available_ollama_model(installed_models)
    payload = build_ollama_command_payload(selected_model, transcript)
    response_payload = request_sender(payload)
    response_text = extract_ollama_text(response_payload)
    if not response_text:
        raise RuntimeError(f"Ollama returned an empty plan for model {selected_model}.")

    return normalize_plan_payload(extract_plan_payload(response_text), selected_model)
