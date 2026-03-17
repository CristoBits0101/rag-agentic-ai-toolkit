# --- DEPENDENCIAS ---
import sys
from pathlib import Path

from langchain_core.messages import AIMessage
from langchain_core.messages import HumanMessage

ROOT = Path(__file__).resolve().parents[2]
SPIKE = ROOT / "spikes" / "18-langchain_tool_calling_math_assistant_lab"

if str(SPIKE) not in sys.path:
    sys.path.insert(0, str(SPIKE))

from models.tool_calling_demo_chat_model import build_tool_calling_math_demo_chat_model
from models.tool_calling_ollama_gateway import select_best_available_ollama_model
from orchestration.tool_calling_agent_orchestration import execute_tool_calling_query
from orchestration.tool_calling_tools_orchestration import add_numbers
from orchestration.tool_calling_tools_orchestration import build_math_assistant_tools
from orchestration.tool_calling_tools_orchestration import calculate_power
from orchestration.tool_calling_tools_orchestration import describe_tool_schemas
from orchestration.tool_calling_tools_orchestration import divide_numbers
from orchestration.tool_calling_tools_orchestration import search_local_reference_fact


class RuleDrivenRealStyleChatModel:
    def __init__(self):
        self._tool_names = set()
        self._call_count = 0

    def bind_tools(self, tools):
        self._tool_names = {tool.name for tool in tools}
        return self

    def invoke(self, messages):
        self._call_count += 1

        if self._call_count == 1:
            return AIMessage(
                content="",
                tool_calls=[
                    {
                        "name": "add_numbers",
                        "args": {"inputs": "25 and 15"},
                        "id": "call_add",
                        "type": "tool_call",
                    }
                ],
            )

        if self._call_count == 2:
            return AIMessage(
                content="",
                tool_calls=[
                    {
                        "name": "multiply_numbers",
                        "args": {"inputs": "40"},
                        "id": "call_multiply",
                        "type": "tool_call",
                    }
                ],
            )

        return AIMessage(content="The final result is 40.")


class RealStyleFactChatModel:
    def __init__(self):
        self._call_count = 0

    def bind_tools(self, tools):
        return self

    def invoke(self, messages):
        self._call_count += 1

        if self._call_count == 1:
            return AIMessage(
                content="",
                tool_calls=[
                    {
                        "name": "search_local_reference_fact",
                        "args": {"query": "population of Canada"},
                        "id": "call_fact",
                        "type": "tool_call",
                    }
                ],
            )

        if self._call_count == 2:
            return AIMessage(
                content="",
                tool_calls=[
                    {
                        "name": "multiply_numbers",
                        "args": {"inputs": "41528680"},
                        "id": "call_multiply_fact",
                        "type": "tool_call",
                    }
                ],
            )

        return AIMessage(content="Canada has around 415 million people.")


def test_describe_tool_schemas_lists_expected_arguments():
    schemas = describe_tool_schemas(build_math_assistant_tools())
    schema_by_name = {schema["name"]: schema for schema in schemas}

    assert "inputs" in schema_by_name["add_numbers"]["args"]
    assert "query" in schema_by_name["search_local_reference_fact"]["args"]


def test_add_numbers_supports_digits_words_and_decimals():
    result = add_numbers.invoke({"inputs": "Add 10, 20.5, two and -3"})

    assert result["numbers"] == [10, 20.5, 2, -3]
    assert result["result"] == 29.5


def test_divide_numbers_reports_division_by_zero():
    result = divide_numbers.invoke({"inputs": "100 5 0"})

    assert result["numbers"] == [100, 5, 0]
    assert result["result"] == "Division by zero is not allowed."


def test_calculate_power_returns_expected_result():
    result = calculate_power.invoke({"inputs": "Raise 3 to the power of 4"})

    assert result["numbers"] == [3, 4]
    assert result["result"] == 81


def test_search_local_reference_fact_returns_canada_population():
    result = search_local_reference_fact.invoke({"query": "What is the population of Canada"})

    assert result["topic"] == "population_of_canada"
    assert result["result"] == 41528680


def test_select_best_available_ollama_model_prefers_ranked_candidate():
    selected_model = select_best_available_ollama_model(
        ["llama3.2:3b", "qwen2.5:7b", "mistral"],
    )

    assert selected_model == "qwen2.5:7b"


def test_demo_model_requests_add_tool_for_two_step_query():
    model = build_tool_calling_math_demo_chat_model()
    bound_model = model.bind_tools(build_math_assistant_tools())

    response = bound_model.invoke(
        [HumanMessage(content="Add 25 and 15 then multiply by 2.")]
    )

    assert response.tool_calls[0]["name"] == "add_numbers"
    assert response.tool_calls[0]["args"] == {"inputs": "25 15"}


def test_execute_tool_calling_query_runs_add_then_multiply():
    result = execute_tool_calling_query(
        "Add 25 and 15 then multiply by 2.",
        model=build_tool_calling_math_demo_chat_model(),
    )

    assert [step.tool_name for step in result.steps] == [
        "add_numbers",
        "multiply_numbers",
    ]
    assert result.steps[0].result["result"] == 40
    assert result.steps[1].result["result"] == 80
    assert result.final_answer == "The final result is 80."


def test_execute_tool_calling_query_corrects_real_model_follow_up_multiply():
    result = execute_tool_calling_query(
        "Add 25 and 15 then multiply by 2.",
        model=RuleDrivenRealStyleChatModel(),
    )

    assert [step.tool_name for step in result.steps] == [
        "add_numbers",
        "multiply_numbers",
    ]
    assert result.steps[1].arguments == {"inputs": "40 2"}
    assert result.steps[1].result["result"] == 80
    assert result.final_answer == "The final result is 80."


def test_execute_tool_calling_query_preserves_subtract_from_order():
    result = execute_tool_calling_query(
        "Subtract 50 from 20.",
        model=build_tool_calling_math_demo_chat_model(),
    )

    assert result.steps[0].tool_name == "subtract_numbers"
    assert result.steps[0].arguments == {"inputs": "20 50"}
    assert result.steps[0].result["result"] == -30
    assert result.final_answer == "The final result is -30."


def test_execute_tool_calling_query_combines_fact_lookup_and_multiplication():
    result = execute_tool_calling_query(
        "What is the population of Canada. Multiply it by 0.75.",
        model=build_tool_calling_math_demo_chat_model(),
    )

    assert [step.tool_name for step in result.steps] == [
        "search_local_reference_fact",
        "multiply_numbers",
    ]
    assert result.steps[0].result["result"] == 41528680
    assert result.steps[1].result["result"] == 31146510
    assert "31146510" in result.final_answer


def test_execute_tool_calling_query_overrides_incorrect_real_model_fact_answer():
    result = execute_tool_calling_query(
        "What is the population of Canada. Multiply it by 0.75.",
        model=RealStyleFactChatModel(),
    )

    assert [step.tool_name for step in result.steps] == [
        "search_local_reference_fact",
        "multiply_numbers",
    ]
    assert result.steps[1].arguments == {"inputs": "41528680 0.75"}
    assert result.steps[1].result["result"] == 31146510
    assert result.final_answer == (
        "Using the local reference fact and the requested multiplier the final result is 31146510."
    )
