# --- DEPENDENCIAS ---
import sys
from pathlib import Path

from langchain_core.messages import AIMessage
from langchain_core.messages import HumanMessage
from langgraph.graph import END

ROOT = Path(__file__).resolve().parents[2]
SPIKE = ROOT / "spikes" / "25-reflection_agent"

if str(SPIKE) not in sys.path:
    sys.path.insert(0, str(SPIKE))

from models.reflection_agent_ollama_gateway import select_best_available_ollama_model
from orchestration.reflection_agent_workflow import build_generation_prompt
from orchestration.reflection_agent_workflow import build_reflection_agent_workflow
from orchestration.reflection_agent_workflow import build_reflection_prompt
from orchestration.reflection_agent_workflow import extract_critiques
from orchestration.reflection_agent_workflow import extract_generated_posts
from orchestration.reflection_agent_workflow import generation_node
from orchestration.reflection_agent_workflow import invoke_reflection_agent
from orchestration.reflection_agent_workflow import normalize_message_sequence
from orchestration.reflection_agent_workflow import reflection_node
from orchestration.reflection_agent_workflow import should_continue


class FakeResponse:
    def __init__(self, content: str):
        self.content = content


class FakeChain:
    def __init__(self, outputs: list[str]):
        self.outputs = outputs
        self.calls: list[dict] = []

    def invoke(self, payload: dict):
        self.calls.append(payload)
        content = self.outputs.pop(0)
        return FakeResponse(content)


def test_build_generation_prompt_contains_messages_placeholder():
    prompt = build_generation_prompt()

    assert "messages" in prompt.input_variables


def test_build_reflection_prompt_contains_messages_placeholder():
    prompt = build_reflection_prompt()

    assert "messages" in prompt.input_variables


def test_generation_node_returns_ai_message():
    chain = FakeChain(["Draft post"])
    result = generation_node([HumanMessage(content="Write a post")], generate_chain=chain)

    assert len(result) == 1
    assert isinstance(result[0], AIMessage)
    assert result[0].content == "Draft post"


def test_reflection_node_returns_human_message_feedback():
    chain = FakeChain(["Add gratitude and a stronger close"])
    result = reflection_node([AIMessage(content="Draft post")], reflect_chain=chain)

    assert len(result) == 1
    assert isinstance(result[0], HumanMessage)
    assert result[0].content == "Add gratitude and a stronger close"


def test_should_continue_routes_to_reflect_until_limit_is_reached():
    assert should_continue([HumanMessage(content="a"), AIMessage(content="b")], max_messages=6) == "reflect"
    assert should_continue([HumanMessage(content=str(index)) for index in range(6)], max_messages=6) == END


def test_extract_generated_posts_and_critiques_parse_message_history():
    messages = [
        HumanMessage(content="Original request"),
        AIMessage(content="Draft 1"),
        HumanMessage(content="Critique 1"),
        AIMessage(content="Draft 2"),
    ]

    assert extract_generated_posts(messages) == ("Draft 1", "Draft 2")
    assert extract_critiques(messages) == ("Critique 1",)


def test_normalize_message_sequence_accepts_message_lists():
    messages = [HumanMessage(content="Original request")]

    assert normalize_message_sequence(messages) == messages


def test_invoke_reflection_agent_runs_three_generation_cycles():
    generate_chain = FakeChain([
        "Draft 1",
        "Draft 2",
        "Final Draft 3",
    ])
    reflect_chain = FakeChain([
        "Critique 1",
        "Critique 2",
    ])
    workflow = build_reflection_agent_workflow(
        generate_chain=generate_chain,
        reflect_chain=reflect_chain,
        max_messages=6,
    )

    result = invoke_reflection_agent("Write a post", workflow=workflow)

    assert result.generated_posts == ("Draft 1", "Draft 2", "Final Draft 3")
    assert result.critiques == ("Critique 1", "Critique 2")
    assert result.final_post == "Final Draft 3"
    assert result.total_messages == 6
    assert "graph TD" in result.mermaid_graph


def test_select_best_available_ollama_model_prefers_ranked_candidate():
    selected_model = select_best_available_ollama_model(
        ["llama3.2:3b", "qwen2.5:7b", "mistral"],
    )

    assert selected_model == "qwen2.5:7b"