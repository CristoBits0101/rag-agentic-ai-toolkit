# --- DEPENDENCIAS ---
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPIKE = ROOT / "spikes" / "36-ag2_tutorial"

if str(SPIKE) not in sys.path:
    sys.path.insert(0, str(SPIKE))

for module_name in list(sys.modules):
    if module_name == "models" or module_name.startswith("models."):
        sys.modules.pop(module_name)
    if module_name == "orchestration" or module_name.startswith("orchestration."):
        sys.modules.pop(module_name)
    if module_name == "config" or module_name.startswith("config."):
        sys.modules.pop(module_name)

from orchestration.ag2_tutorial_workflow import built_in_agent_demo
from orchestration.ag2_tutorial_workflow import conversational_agent_demo
from orchestration.ag2_tutorial_workflow import group_chat_lesson_planning_demo
from orchestration.ag2_tutorial_workflow import human_in_the_loop_demo
from orchestration.ag2_tutorial_workflow import structured_outputs_demo
from orchestration.ag2_tutorial_workflow import tools_and_extensions_demo


def test_conversational_agent_demo_returns_neural_network_summary():
    result = conversational_agent_demo()

    assert "neural network" in result.summary.lower()


def test_built_in_agent_demo_creates_svg_artifact():
    result, artifact_path = built_in_agent_demo()

    assert artifact_path.exists()
    assert "executed" in result.summary.lower() or "artifact" in result.summary.lower()


def test_human_in_the_loop_demo_returns_three_triage_records():
    outputs = human_in_the_loop_demo()

    assert len(outputs) == 3
    assert all("assistant" in item for item in outputs)


def test_group_chat_demo_finishes_with_done_signal():
    result = group_chat_lesson_planning_demo()

    assert "done" in result.summary.lower()


def test_tools_and_structured_output_demos_are_deterministic():
    tool_result = tools_and_extensions_demo()
    structured = structured_outputs_demo()

    assert "72" in tool_result.summary
    assert structured["customer_name"] == "John Doe"
    assert structured["urgency_level"] == "High"