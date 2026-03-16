# --- DEPENDENCIAS ---
from config.voice_desktop_config import USE_OLLAMA_BY_DEFAULT
from models.voice_agent_demo_planner import build_demo_action_plan
from models.voice_agent_ollama_gateway import plan_voice_command_with_ollama
from models.voice_desktop_entities import VoiceActionPlan


def build_voice_action_plan(
    transcript: str,
    prefer_ollama: bool = USE_OLLAMA_BY_DEFAULT,
) -> VoiceActionPlan:
    if prefer_ollama:
        try:
            return plan_voice_command_with_ollama(transcript)
        except Exception:
            pass

    return build_demo_action_plan(transcript)
