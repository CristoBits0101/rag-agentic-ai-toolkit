# --- DEPENDENCIAS ---
import sys
from pathlib import Path

from langchain_core.messages import AIMessage
from langchain_core.messages import HumanMessage
from langchain_core.messages import ToolMessage

ROOT = Path(__file__).resolve().parents[2]
SPIKE = ROOT / "spikes" / "27-react_langgraph_agents"

if str(SPIKE) not in sys.path:
    sys.path.insert(0, str(SPIKE))

from models.react_agent_ollama_gateway import select_best_available_ollama_model
from orchestration.react_agent_orchestration import extract_tool_steps
from orchestration.react_agent_orchestration import get_final_answer
from orchestration.react_agent_orchestration import invoke_react_query
from orchestration.react_agent_orchestration import should_continue
from orchestration.react_tools_orchestration import build_tools_by_name
from orchestration.react_tools_orchestration import calculator_tool
from orchestration.react_tools_orchestration import describe_tool_schemas
from orchestration.react_tools_orchestration import news_summarizer_tool
from orchestration.react_tools_orchestration import recommend_clothing
from orchestration.react_tools_orchestration import search_tool
from orchestration.react_tools_orchestration import tool


class FakeBoundModel:
    def __init__(self, responses):
        self._responses = responses

    def invoke(self, payload):
        return self._responses.pop(0)


class FakeModel:
    def __init__(self, responses):
        self.responses = responses

    def bind_tools(self, tools):
        return FakeBoundModel(self.responses)


def test_recommend_clothing_handles_cold_weather():
    result = recommend_clothing.invoke({"weather": "Overcast and cold around 50F"})

    assert result == "Wear a warm jacket or sweater."


def test_calculator_tool_evaluates_percentage_and_square_root():
    result = calculator_tool.invoke({"expression": "15% of 250 plus square root of 144"})

    assert result == "49.5"


def test_news_summarizer_tool_formats_top_articles():
    raw_content = '[{"title":"AI launch","content":"A new model was released.","url":"https://example.com/a"}]'
    result = news_summarizer_tool.invoke({"news_content": raw_content})

    assert "1. AI launch" in result
    assert "https://example.com/a" in result


def test_should_continue_routes_based_on_tool_calls():
    assert should_continue({"messages": [AIMessage(content="done")]}) == "end"
    assert should_continue({"messages": [AIMessage(content="", tool_calls=[{"name": "search_tool", "args": {"query": "weather"}, "id": "1", "type": "tool_call"}])]}) == "continue"


def test_extract_tool_steps_reads_tool_call_and_result():
    messages = (
        HumanMessage(content="question"),
        AIMessage(
            content="",
            tool_calls=[
                {"name": "recommend_clothing", "args": {"weather": "cold"}, "id": "call_1", "type": "tool_call"}
            ],
        ),
        ToolMessage(content='"Wear a warm jacket or sweater."', name="recommend_clothing", tool_call_id="call_1"),
        AIMessage(content="Final answer."),
    )

    steps = extract_tool_steps(messages)

    assert steps[0].tool_name == "recommend_clothing"
    assert steps[0].arguments == {"weather": "cold"}
    assert steps[0].result == "Wear a warm jacket or sweater."


def test_get_final_answer_returns_last_non_tool_ai_message():
    messages = (
        HumanMessage(content="question"),
        AIMessage(content="", tool_calls=[{"name": "search_tool", "args": {"query": "weather"}, "id": "1", "type": "tool_call"}]),
        ToolMessage(content="[]", name="search_tool", tool_call_id="1"),
        AIMessage(content="Final answer here."),
    )

    assert get_final_answer(messages) == "Final answer here."


def test_invoke_react_query_runs_with_fake_model_and_tools():
    fake_model = FakeModel(
        [
            AIMessage(
                content="",
                tool_calls=[
                    {"name": "recommend_clothing", "args": {"weather": "cold and rainy"}, "id": "call_1", "type": "tool_call"}
                ],
            ),
            AIMessage(content="It is cold and rainy so bring a raincoat and something warm."),
        ]
    )
    tools = [recommend_clothing]

    result = invoke_react_query("What should I wear?", model=fake_model, tools=tools)

    assert result.final_answer == "It is cold and rainy so bring a raincoat and something warm."
    assert result.steps[0].tool_name == "recommend_clothing"
    assert "graph TD" in result.mermaid_graph


def test_describe_tool_schemas_lists_calculator_and_news_tools():
    schemas = describe_tool_schemas()
    names = {schema["name"] for schema in schemas}

    assert "calculator_tool" in names
    assert "news_summarizer_tool" in names


def test_select_best_available_ollama_model_prefers_ranked_candidate():
    selected_model = select_best_available_ollama_model(["llama3.2:3b", "qwen2.5:7b", "mistral"])

    assert selected_model == "qwen2.5:7b"