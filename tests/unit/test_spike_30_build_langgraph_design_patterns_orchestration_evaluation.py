# --- DEPENDENCIAS ---
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPIKE = ROOT / "spikes" / "30-build_langgraph_design_patterns_orchestration_evaluation"

if str(SPIKE) not in sys.path:
    sys.path.insert(0, str(SPIKE))

for module_name in list(sys.modules):
    if module_name == "models" or module_name.startswith("models."):
        sys.modules.pop(module_name)
    if module_name == "orchestration" or module_name.startswith("orchestration."):
        sys.modules.pop(module_name)
    if module_name == "config" or module_name.startswith("config."):
        sys.modules.pop(module_name)

from orchestration.orchestrator_worker_workflow import invoke_orchestrator_worker
from orchestration.reflection_workflow import invoke_reflection_workflow


class FakeResponse:
    def __init__(self, content: str):
        self.content = content


class FakeModel:
    def invoke(self, prompt: str):
        lowered = prompt.lower()
        if "world class chef" in lowered and "steak and eggs" in lowered:
            return FakeResponse("Chef from American cuisine explaining steak and eggs.")
        if "world class chef" in lowered and "tacos" in lowered:
            return FakeResponse("Chef from Mexican cuisine explaining tacos.")
        if "world class chef" in lowered and "chili" in lowered:
            return FakeResponse("Chef from Tex-Mex cuisine explaining chili.")
        if "ray dalio" in lowered:
            return FakeResponse("Balanced plan with equities bonds and diversification.")
        return FakeResponse("Aggressive growth plan with technology equity exposure.")


def test_orchestrator_worker_workflow_builds_final_guide():
    result = invoke_orchestrator_worker("steak and eggs tacos and chili", FakeModel())
    assert "steak and eggs" in result["final_meal_guide"].lower()
    assert "tacos" in result["final_meal_guide"].lower()


def test_reflection_workflow_reaches_target_grade_or_stops_cleanly():
    result = invoke_reflection_workflow(
        "Age: 29\nSalary: $110000\nAssets: $40000\nGoal: Financial independence\nRisk tolerance: High",
        FakeModel(),
    )
    assert result["target_grade"] == "aggressive"
    assert result["n"] >= 1
    assert result["investment_plan"]