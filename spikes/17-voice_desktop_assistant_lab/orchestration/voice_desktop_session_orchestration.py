# --- DEPENDENCIAS ---
import unicodedata

from config.voice_desktop_config import CANCELLATION_KEYWORDS
from config.voice_desktop_config import CONFIRMATION_KEYWORDS
from config.voice_desktop_config import EXIT_KEYWORDS
from models.voice_desktop_entities import VoiceActionPlan
from models.voice_desktop_entities import VoiceExecutionResult
from orchestration.voice_desktop_execution_orchestration import execute_voice_action
from orchestration.voice_desktop_planning_orchestration import build_voice_action_plan


def normalize_transcript(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text or "")
    return normalized.encode("ascii", "ignore").decode("ascii").lower().strip()


def should_exit_session(transcript: str) -> bool:
    normalized = normalize_transcript(transcript)
    return normalized in EXIT_KEYWORDS


def classify_confirmation(transcript: str) -> bool | None:
    normalized = normalize_transcript(transcript)
    if normalized in CONFIRMATION_KEYWORDS:
        return True

    if normalized in CANCELLATION_KEYWORDS:
        return False

    return None


def process_voice_transcript(
    transcript: str,
    pending_plan: VoiceActionPlan | None = None,
    prefer_ollama: bool = True,
) -> tuple[VoiceExecutionResult, VoiceActionPlan | None]:
    if not transcript.strip():
        return (
            VoiceExecutionResult(
                success=False,
                message="No he recibido ninguna orden.",
                action="no_op",
            ),
            pending_plan,
        )

    if pending_plan is not None:
        confirmation = classify_confirmation(transcript)
        if confirmation is True:
            return execute_voice_action(pending_plan), None

        if confirmation is False:
            return (
                VoiceExecutionResult(
                    success=True,
                    message="Accion cancelada.",
                    action=pending_plan.action,
                ),
                None,
            )

        return (
            VoiceExecutionResult(
                success=False,
                message="Necesito que digas confirmar o cancelar.",
                action=pending_plan.action,
            ),
            pending_plan,
        )

    plan = build_voice_action_plan(transcript, prefer_ollama=prefer_ollama)
    if plan.requires_confirmation:
        return (
            VoiceExecutionResult(
                success=True,
                message=plan.confirmation_prompt,
                action=plan.action,
            ),
            plan,
        )

    return execute_voice_action(plan), None
