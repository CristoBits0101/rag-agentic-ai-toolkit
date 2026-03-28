# --- DEPENDENCIAS ---
import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPIKE = ROOT / "spikes" / "35-beeai_agentic_systems"

if str(SPIKE) not in sys.path:
    sys.path.insert(0, str(SPIKE))

for module_name in list(sys.modules):
    if module_name == "models" or module_name.startswith("models."):
        sys.modules.pop(module_name)
    if module_name == "orchestration" or module_name.startswith("orchestration."):
        sys.modules.pop(module_name)
    if module_name == "config" or module_name.startswith("config."):
        sys.modules.pop(module_name)

from orchestration.beeai_tutorial_workflow import BusinessPlan
from orchestration.beeai_tutorial_workflow import SimpleCalculatorTool
from orchestration.beeai_tutorial_workflow import SimplePromptTemplate
from orchestration.beeai_tutorial_workflow import basic_chat_example
from orchestration.beeai_tutorial_workflow import calculator_agent_example
from orchestration.beeai_tutorial_workflow import configure_environment
from orchestration.beeai_tutorial_workflow import controlled_execution_example
from orchestration.beeai_tutorial_workflow import multi_agent_travel_planner_with_language
from orchestration.beeai_tutorial_workflow import structured_output_example


def test_environment_configuration_sets_project_id():
    message = configure_environment()

    assert message == "Environment configured successfully!"


def test_prompt_template_renders_values():
    template = SimplePromptTemplate("Project {{name}} solves {{problem}}")

    assert template.render({"name": "A", "problem": "B"}) == "Project A solves B"


def test_basic_chat_returns_food_delivery_idea():
    response = asyncio.run(basic_chat_example())

    assert "micro kitchen" in response.lower() or "hyperlocal" in response.lower()


def test_structured_output_contains_business_plan_fields():
    payload = asyncio.run(structured_output_example())

    assert set(BusinessPlan.model_fields).issubset(payload.keys())


def test_calculator_tool_and_agent_example_produce_expected_results():
    tool = SimpleCalculatorTool()
    output = asyncio.run(tool.run(tool.input_schema(expression="15 + 5")))
    results = asyncio.run(calculator_agent_example())

    assert "Result: 20" in output.text
    assert any("Result: 42" in entry for entry in results)


def test_controlled_execution_records_permission_free_tool_sequence():
    result = asyncio.run(controlled_execution_example())

    assert result.trajectory[0].startswith("ThinkTool")
    assert any(entry.startswith("WikipediaTool") for entry in result.trajectory)


def test_multi_agent_travel_planner_returns_all_guidance_sections():
    summary = asyncio.run(multi_agent_travel_planner_with_language())

    assert "Tokyo" in summary.destination_guidance or "Tokyo" in summary.coordinator_summary
    assert "weather" in summary.weather_guidance.lower() or "mild" in summary.weather_guidance.lower()
    assert "polite" in summary.language_guidance.lower() or "etiquette" in summary.language_guidance.lower()