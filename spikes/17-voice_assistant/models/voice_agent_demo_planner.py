# --- DEPENDENCIAS ---
import re
import unicodedata

from config.voice_desktop_config import DEFAULT_CONFIRMATION_PROMPT
from config.voice_desktop_config import SENSITIVE_ACTIONS
from data.voice_command_catalog import APPLICATION_ALIASES
from data.voice_command_catalog import HOTKEY_ALIASES
from data.voice_command_catalog import KNOWN_URLS
from models.voice_desktop_entities import VoiceActionPlan


def normalize_text(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text or "")
    return normalized.encode("ascii", "ignore").decode("ascii").lower().strip()


def extract_quoted_value(text: str) -> str | None:
    match = re.search(r'"([^"]+)"|\'([^\']+)\'', text)
    if not match:
        return None

    return next(group for group in match.groups() if group)


def extract_text_to_type(transcript: str) -> str | None:
    quoted_value = extract_quoted_value(transcript)
    if quoted_value:
        return quoted_value.strip()

    match = re.search(r"(?i)(?:escribe|teclea)\s+(.+)", transcript)
    if not match:
        return None

    return match.group(1).strip()


def extract_path_candidate(transcript: str) -> str | None:
    quoted_value = extract_quoted_value(transcript)
    if quoted_value:
        return quoted_value.strip()

    path_match = re.search(r"[a-zA-Z]:\\[^\"\n]+", transcript)
    if path_match:
        return path_match.group(0).strip()

    tail_match = re.search(r"(?i)(?:borra|elimina|manda a la papelera)\s+(.+)", transcript)
    if not tail_match:
        return None

    return tail_match.group(1).strip()


def normalize_url(url: str) -> str:
    cleaned = url.strip()
    if cleaned.startswith(("http://", "https://")):
        return cleaned

    return f"https://{cleaned}"


def extract_url_candidate(transcript: str) -> str | None:
    quoted_value = extract_quoted_value(transcript)
    if quoted_value and ("." in quoted_value or quoted_value.startswith("http")):
        return normalize_url(quoted_value)

    normalized = normalize_text(transcript)
    for keyword, url in KNOWN_URLS.items():
        if keyword in normalized:
            return url

    match = re.search(r"(?i)(https?://\S+|www\.\S+|[a-z0-9-]+\.(?:com|dev|es|io|net|org))", transcript)
    if not match:
        return None

    return normalize_url(match.group(0))


def resolve_application_name(transcript: str) -> str | None:
    normalized = normalize_text(transcript)
    for alias, application_name in APPLICATION_ALIASES.items():
        if alias in normalized:
            return application_name

    return None


def extract_hotkey_keys(transcript: str) -> list[str]:
    quoted_value = extract_quoted_value(transcript)
    source = normalize_text(quoted_value or transcript)
    keys: list[str] = []

    for raw_token in re.split(r"[\s\+\-]+", source):
        token = HOTKEY_ALIASES.get(raw_token, raw_token)
        if token in {"alt", "ctrl", "delete", "enter", "esc", "shift", "tab", "win"}:
            keys.append(token)
        elif len(token) == 1 and token.isalnum():
            keys.append(token)

    return keys


def build_answer_plan(message: str) -> VoiceActionPlan:
    return VoiceActionPlan(
        action="answer",
        response=message,
        planner_provider="demo",
        planner_model="rule_based",
    )


def build_demo_action_plan(transcript: str) -> VoiceActionPlan:
    normalized = normalize_text(transcript)
    if not normalized:
        return VoiceActionPlan(action="no_op", response="No he escuchado ninguna orden.")

    if any(keyword in normalized for keyword in ("cierra", "cerrar", "cierre", "termina", "finaliza")):
        application_name = resolve_application_name(transcript)
        if not application_name:
            return build_answer_plan("No he detectado una aplicacion permitida para cerrar.")

        return VoiceActionPlan(
            action="close_application",
            parameters={"application": application_name},
            response=f"Voy a cerrar {application_name}.",
            requires_confirmation=True,
            confirmation_prompt=f"Quieres cerrar {application_name}. Di confirmar o cancelar.",
            planner_provider="demo",
            planner_model="rule_based",
        )

    if any(keyword in normalized for keyword in ("borra", "elimina", "papelera")):
        path_value = extract_path_candidate(transcript)
        if not path_value:
            return build_answer_plan("No he detectado una ruta valida para enviar a la papelera.")

        return VoiceActionPlan(
            action="trash_path",
            parameters={"path": path_value},
            response=f"Voy a enviar a la papelera {path_value}.",
            requires_confirmation=True,
            confirmation_prompt=f"Quieres enviar a la papelera {path_value}. Di confirmar o cancelar.",
            planner_provider="demo",
            planner_model="rule_based",
        )

    if any(keyword in normalized for keyword in ("escribe", "teclea")):
        text_value = extract_text_to_type(transcript)
        if not text_value:
            return build_answer_plan("No he detectado el texto que quieres escribir.")

        return VoiceActionPlan(
            action="type_text",
            parameters={"text": text_value},
            response=f"Voy a escribir el texto solicitado: {text_value}.",
            planner_provider="demo",
            planner_model="rule_based",
        )

    if any(keyword in normalized for keyword in ("pulsa", "presiona", "atajo")):
        keys = extract_hotkey_keys(transcript)
        if not keys:
            return build_answer_plan("No he detectado un atajo de teclado compatible.")

        return VoiceActionPlan(
            action="press_hotkey",
            parameters={"keys": keys},
            response=f"Voy a pulsar el atajo {' + '.join(keys)}.",
            planner_provider="demo",
            planner_model="rule_based",
        )

    if any(keyword in normalized for keyword in ("abre", "abrir", "lanzar", "ejecuta")):
        url_value = extract_url_candidate(transcript)
        if url_value:
            return VoiceActionPlan(
                action="open_url",
                parameters={"url": url_value},
                response=f"Voy a abrir {url_value}.",
                planner_provider="demo",
                planner_model="rule_based",
            )

        application_name = resolve_application_name(transcript)
        if application_name:
            return VoiceActionPlan(
                action="open_application",
                parameters={"application": application_name},
                response=f"Voy a abrir {application_name}.",
                planner_provider="demo",
                planner_model="rule_based",
            )

    if any(keyword in normalized for keyword in ("que puedes hacer", "ayuda", "help")):
        return build_answer_plan(
            "Puedo abrir y cerrar aplicaciones permitidas abrir urls escribir texto pulsar atajos y enviar archivos a la papelera con confirmacion."
        )

    plan = build_answer_plan("No he encontrado una accion segura para esa orden.")
    if plan.action in SENSITIVE_ACTIONS:
        plan.requires_confirmation = True
        plan.confirmation_prompt = DEFAULT_CONFIRMATION_PROMPT

    return plan
