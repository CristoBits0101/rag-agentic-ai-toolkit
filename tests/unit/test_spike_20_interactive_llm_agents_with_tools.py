# --- DEPENDENCIAS ---
import sys
from pathlib import Path

from langchain_core.messages import AIMessage
from langchain_core.messages import HumanMessage

ROOT = Path(__file__).resolve().parents[2]
SPIKE = ROOT / "spikes" / "20-interactive_llm_agents_with_tools_lab"

if str(SPIKE) not in sys.path:
    sys.path.insert(0, str(SPIKE))

from models.interactive_agents_ollama_gateway import select_best_available_ollama_model
from orchestration.interactive_agents_agent_orchestration import TipAgent
from orchestration.interactive_agents_agent_orchestration import ToolCallingAgent
from orchestration.interactive_agents_manual_tool_calling_orchestration import (
    execute_manual_tool_calling_query,
)
from orchestration.interactive_agents_manual_tool_calling_orchestration import (
    execute_parsed_tool_calls,
)
from orchestration.interactive_agents_manual_tool_calling_orchestration import (
    extract_tool_calls_from_ai_message,
)
from orchestration.interactive_agents_tools_orchestration import add
from orchestration.interactive_agents_tools_orchestration import build_interactive_math_tools
from orchestration.interactive_agents_tools_orchestration import build_interactive_tools
from orchestration.interactive_agents_tools_orchestration import build_tip_tools
from orchestration.interactive_agents_tools_orchestration import build_tool_map
from orchestration.interactive_agents_tools_orchestration import calculate_tip
from orchestration.interactive_agents_tools_orchestration import describe_tool_schemas


class AddThenAnswerModel:
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
                        "name": "add",
                        "args": {"a": 3, "b": 2},
                        "id": "call_add",
                        "type": "tool_call",
                    }
                ],
            )

        return AIMessage(content="The final result is 5.")


class RetryThenAddModel:
    def __init__(self):
        self._call_count = 0

    def bind_tools(self, tools):
        return self

    def invoke(self, messages):
        self._call_count += 1

        if self._call_count == 1:
            return AIMessage(content="I can solve that.")

        if self._call_count == 2:
            assert isinstance(messages[-1], HumanMessage)
            return AIMessage(
                content="",
                tool_calls=[
                    {
                        "name": "add",
                        "args": {"a": 8, "b": 1},
                        "id": "call_retry_add",
                        "type": "tool_call",
                    }
                ],
            )

        return AIMessage(content="")


class TipToolModel:
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
                        "name": "calculate_tip",
                        "args": {"total_bill": 60.0, "tip_percent": 20.0},
                        "id": "call_tip",
                        "type": "tool_call",
                    }
                ],
            )

        return AIMessage(content="")


def test_describe_tool_schemas_lists_expected_fields():
    schemas = describe_tool_schemas()
    schema_by_name = {schema["name"]: schema for schema in schemas}

    assert "a" in schema_by_name["add"]["args"]
    assert "b" in schema_by_name["multiply"]["args"]
    assert "total_bill" in schema_by_name["calculate_tip"]["args"]


def test_add_and_tip_tools_return_expected_values():
    assert add.invoke({"a": 1, "b": 2}) == 3
    assert calculate_tip.invoke({"total_bill": 120, "tip_percent": 15}) == {
        "total_bill": 120,
        "tip_percent": 15,
        "tip_amount": 18.0,
        "total_with_tip": 138.0,
    }


def test_build_tool_map_contains_registered_tool_names():
    tool_map = build_tool_map(build_interactive_tools())

    assert set(tool_map) == {"add", "subtract", "multiply", "calculate_tip"}


def test_extract_tool_calls_from_ai_message_reads_name_args_and_id():
    response = AIMessage(
        content="",
        tool_calls=[
            {
                "name": "add",
                "args": {"a": 3, "b": 2},
                "id": "call_add",
                "type": "tool_call",
            }
        ],
    )

    parsed_tool_calls = extract_tool_calls_from_ai_message(response)

    assert parsed_tool_calls[0].tool_name == "add"
    assert parsed_tool_calls[0].arguments == {"a": 3, "b": 2}
    assert parsed_tool_calls[0].tool_call_id == "call_add"


def test_execute_parsed_tool_calls_supports_multiple_calls_in_one_message():
    tool_map = build_tool_map(build_interactive_math_tools())
    parsed_tool_calls = extract_tool_calls_from_ai_message(
        AIMessage(
            content="",
            tool_calls=[
                {
                    "name": "add",
                    "args": {"a": 3, "b": 2},
                    "id": "call_add",
                    "type": "tool_call",
                },
                {
                    "name": "multiply",
                    "args": {"a": 4, "b": 5},
                    "id": "call_multiply",
                    "type": "tool_call",
                },
            ],
        )
    )

    steps, tool_messages = execute_parsed_tool_calls(parsed_tool_calls, tool_map)

    assert steps[0].result == {"result": 5}
    assert steps[1].result == {"result": 20}
    assert len(tool_messages) == 2


def test_execute_manual_tool_calling_query_runs_add_flow():
    result = execute_manual_tool_calling_query(
        "What is 3 + 2?",
        tools=build_interactive_math_tools(),
        model=AddThenAnswerModel(),
    )

    assert [tool_call.tool_name for tool_call in result.tool_calls] == ["add"]
    assert [step.tool_name for step in result.steps] == ["add"]
    assert result.steps[0].result == {"result": 5}
    assert result.final_answer == "The final result is 5."


def test_execute_manual_tool_calling_query_retries_when_model_skips_tool_call():
    result = execute_manual_tool_calling_query(
        "What is 8 + 1?",
        tools=build_interactive_math_tools(),
        model=RetryThenAddModel(),
    )

    assert [tool_call.tool_name for tool_call in result.tool_calls] == ["add"]
    assert result.steps[0].result == {"result": 9}
    assert result.final_answer == "The final result is 9."


def test_tool_calling_agent_returns_arithmetic_answer():
    agent = ToolCallingAgent(
        model=AddThenAnswerModel(),
        tools=build_interactive_math_tools(),
    )

    assert agent.run("What is 3 + 2?") == "The final result is 5."


def test_tip_agent_uses_tip_tool_and_fallback_final_answer():
    agent = TipAgent(
        model=TipToolModel(),
        tools=build_tip_tools(),
    )

    assert agent.run("How much should I tip on $60 at 20%?") == (
        "The tip amount is 12 and the total with tip is 72."
    )


def test_select_best_available_ollama_model_prefers_ranked_candidate():
    selected_model = select_best_available_ollama_model(
        ["llama3.2:3b", "qwen2.5:7b", "mistral"],
    )

    assert selected_model == "qwen2.5:7b"
