# --- DEPENDENCIAS ---
from config.voice_desktop_config import USE_OLLAMA_BY_DEFAULT
from models.voice_agent_demo_planner import build_rule_based_action_plan
from models.voice_agent_ollama_gateway import plan_voice_command_with_ollama
from models.voice_desktop_entities import VoiceActionPlan


def build_voice_action_plan(
    transcript: str,
    prefer_ollama: bool = USE_OLLAMA_BY_DEFAULT,
) -> VoiceActionPlan:
    direct_plan = build_rule_based_action_plan(transcript)
    if direct_plan is not None:
        return direct_plan

    if not prefer_ollama:
        raise RuntimeError("Practica 17 requiere Ollama para planificar acciones de escritorio.")

    return plan_voice_command_with_ollama(transcript)
