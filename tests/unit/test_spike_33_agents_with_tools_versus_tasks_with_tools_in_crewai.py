# --- DEPENDENCIAS ---
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPIKE = ROOT / "spikes" / "33-agents_with_tools_versus_tasks_with_tools_in_crewai"

if str(SPIKE) not in sys.path:
    sys.path.insert(0, str(SPIKE))

for module_name in list(sys.modules):
    if module_name == "models" or module_name.startswith("models."):
        sys.modules.pop(module_name)
    if module_name == "orchestration" or module_name.startswith("orchestration."):
        sys.modules.pop(module_name)
    if module_name == "config" or module_name.startswith("config."):
        sys.modules.pop(module_name)

from orchestration.daily_dish_chatbot_workflow import build_task_centric_crew
from orchestration.daily_dish_chatbot_workflow import compare_tool_assignment
from orchestration.daily_dish_chatbot_workflow import run_custom_tools_demo


class FakeResponse:
    def __init__(self, content: str):
        self.content = content


class FakeModel:
    def invoke(self, prompt: str):
        lowered = prompt.lower()
        if "warm customer service tone" in lowered:
            return FakeResponse("The Daily Dish is open daily with extended weekend hours and I can also share details beyond the FAQ when needed.")
        if "draft the final response" in lowered:
            return FakeResponse("The Daily Dish is open Monday through Thursday from 11 AM to 9 PM and Friday through Sunday from 10 AM to 10 PM.")
        return FakeResponse("Structured answer.")


def test_compare_tool_assignment_shows_task_centric_uses_fewer_tools_for_simple_faq_query():
    summary = compare_tool_assignment(query="What are your timings?", model=FakeModel())

    assert "faq_search_tool" in summary.agent_centric_tools
    assert "web_search_tool" in summary.agent_centric_tools
    assert summary.task_centric_tools == ["faq_search_tool"]


def test_task_centric_crew_exposes_three_stages():
    crew = build_task_centric_crew(model=FakeModel())
    result = crew.kickoff(inputs={"customer_query": "Where are you located and is there parking nearby?"})

    assert len(result.tasks_output) == 3
    assert "web_search_tool" in result.tasks_output[1].raw


def test_custom_tools_demo_returns_sum_and_product():
    demo = run_custom_tools_demo(model=FakeModel())

    assert demo.addition_result == 15
    assert demo.multiplication_result == 5040