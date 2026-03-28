# --- DEPENDENCIAS ---
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPIKE = ROOT / "spikes" / "37-ag2_healthcare_chatbot"

if str(SPIKE) not in sys.path:
    sys.path.insert(0, str(SPIKE))

for module_name in list(sys.modules):
    if module_name == "models" or module_name.startswith("models."):
        sys.modules.pop(module_name)
    if module_name == "orchestration" or module_name.startswith("orchestration."):
        sys.modules.pop(module_name)
    if module_name == "config" or module_name.startswith("config."):
        sys.modules.pop(module_name)

from orchestration.healthcare_chatbot_workflow import build_healthcare_agents
from orchestration.healthcare_chatbot_workflow import run_automed_consultation
from orchestration.healthcare_chatbot_workflow import run_mental_health_chatbot


def test_healthcare_agents_are_created_in_expected_order():
    agents = build_healthcare_agents()

    assert [agent.name for agent in agents] == ["patient", "diagnosis", "pharmacy", "consultation"]


def test_automed_consultation_reaches_consultation_complete():
    result = run_automed_consultation("persistent headaches fatigue and dizziness")

    assert "CONSULTATION_COMPLETE" in result.summary
    assert "Possible causes" in result.summary


def test_mental_health_chatbot_returns_emotion_and_therapy_guidance():
    result = run_mental_health_chatbot("I feel overwhelmed stressed and I am not sleeping well.")

    assert "stress" in result.summary.lower() or "anxiety" in result.summary.lower()
    assert "breathing" in result.summary.lower() or "journaling" in result.summary.lower()