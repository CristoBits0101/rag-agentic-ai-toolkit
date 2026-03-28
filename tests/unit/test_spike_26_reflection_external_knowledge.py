# --- DEPENDENCIAS ---
import json
import sys
from pathlib import Path

from langchain_core.messages import AIMessage
from langchain_core.messages import HumanMessage
from langchain_core.messages import ToolMessage
from langgraph.graph import END

ROOT = Path(__file__).resolve().parents[2]
SPIKE = ROOT / "spikes" / "26-reflection_external_knowledge"

if str(SPIKE) not in sys.path:
    sys.path.insert(0, str(SPIKE))

from models.external_knowledge_gateway import ExternalKnowledgeResearchTool
from models.external_reflection_ollama_gateway import select_best_available_ollama_model
from orchestration.external_reflection_agent_workflow import build_external_reflection_graph
from orchestration.external_reflection_agent_workflow import build_prompt_template
from orchestration.external_reflection_agent_workflow import event_loop
from orchestration.external_reflection_agent_workflow import execute_tools
from orchestration.external_reflection_agent_workflow import extract_structured_tool_args
from orchestration.external_reflection_agent_workflow import invoke_external_reflection_agent
from orchestration.external_reflection_agent_workflow import respond_node
from orchestration.external_reflection_agent_workflow import revise_node


class FakeResponse:
    def __init__(self, tool_call_name: str, args: dict):
        self.content = ""
        self.tool_calls = [
            {
                "name": tool_call_name,
                "args": args,
                "id": f"call_{tool_call_name.lower()}",
                "type": "tool_call",
            }
        ]


class FakeChain:
    def __init__(self, responses: list[FakeResponse]):
        self.responses = responses
        self.calls: list[dict] = []

    def invoke(self, payload: dict):
        self.calls.append(payload)
        return self.responses.pop(0)


class FakeResearchTool:
    def __init__(self):
        self.queries: list[list[str]] = []

    def search_many(self, queries: list[str]) -> dict[str, list[dict[str, str]]]:
        self.queries.append(queries)
        return {
            query: [
                {
                    "title": f"Evidence for {query}",
                    "url": f"https://example.com/{index}",
                    "snippet": "Structured evidence.",
                    "source": "test",
                }
            ]
            for index, query in enumerate(queries, start=1)
        }


def test_build_prompt_template_contains_messages_placeholder():
    prompt = build_prompt_template()

    assert "messages" in prompt.input_variables


def test_respond_node_invokes_responder_chain():
    chain = FakeChain(
        [
            FakeResponse(
                "AnswerQuestion",
                {
                    "answer": "Initial answer.",
                    "reflection": {"missing": "Citations", "superfluous": "None"},
                    "search_queries": ["prediabetes breakfast evidence"],
                },
            )
        ]
    )

    result = respond_node([HumanMessage(content="question")], responder_chain=chain)

    assert len(result) == 1
    assert result[0].tool_calls[0]["name"] == "AnswerQuestion"


def test_execute_tools_serializes_search_results_into_tool_message():
    research_tool = FakeResearchTool()
    state = [
        HumanMessage(content="question"),
        AIMessage(
            content="",
            tool_calls=[
                {
                    "name": "AnswerQuestion",
                    "args": {"search_queries": ["healthy breakfast prediabetes"]},
                    "id": "call_answer",
                    "type": "tool_call",
                }
            ],
        ),
    ]

    result = execute_tools(state, research_tool=research_tool)

    assert len(result) == 1
    assert isinstance(result[0], ToolMessage)
    payload = json.loads(result[0].content)
    assert "healthy breakfast prediabetes" in payload


def test_revise_node_invokes_revisor_chain():
    chain = FakeChain(
        [
            FakeResponse(
                "ReviseAnswer",
                {
                    "answer": "Revised answer.",
                    "reflection": {"missing": "None", "superfluous": "None"},
                    "search_queries": ["fiber cardiovascular outcomes"],
                    "references": ["https://example.com/1"],
                },
            )
        ]
    )

    result = revise_node([HumanMessage(content="question")], revisor_chain=chain)

    assert len(result) == 1
    assert result[0].tool_calls[0]["name"] == "ReviseAnswer"


def test_event_loop_stops_after_max_tool_messages():
    state = [ToolMessage(content="{}", tool_call_id=f"call_{index}") for index in range(3)]
    active_state = [
        ToolMessage(content="{}", tool_call_id="call_1"),
        ToolMessage(content="{}", tool_call_id="call_2"),
        AIMessage(
            content="",
            tool_calls=[
                {
                    "name": "ReviseAnswer",
                    "args": {"search_queries": ["glycemic breakfast trial"]},
                    "id": "call_revise",
                    "type": "tool_call",
                }
            ],
        ),
    ]

    assert event_loop(state, max_iterations=3) == END
    assert event_loop(active_state, max_iterations=3) == "execute_tools"


def test_extract_structured_tool_args_reads_answers_from_messages():
    messages = [
        AIMessage(
            content="",
            tool_calls=[
                {
                    "name": "AnswerQuestion",
                    "args": {"answer": "Initial answer", "search_queries": []},
                    "id": "call_1",
                    "type": "tool_call",
                }
            ],
        ),
        AIMessage(
            content="",
            tool_calls=[
                {
                    "name": "ReviseAnswer",
                    "args": {"answer": "Final answer", "search_queries": [], "references": ["https://example.com"]},
                    "id": "call_2",
                    "type": "tool_call",
                }
            ],
        ),
    ]

    result = extract_structured_tool_args(messages)

    assert result[0]["answer"] == "Initial answer"
    assert result[1]["answer"] == "Final answer"


def test_invoke_external_reflection_agent_collects_initial_and_final_answers():
    responder_chain = FakeChain(
        [
            FakeResponse(
                "AnswerQuestion",
                {
                    "answer": "Initial answer.",
                    "reflection": {"missing": "Need citations.", "superfluous": "Too generic."},
                    "search_queries": ["prediabetes breakfast randomized trial"],
                },
            )
        ]
    )
    revisor_chain = FakeChain(
        [
            FakeResponse(
                "ReviseAnswer",
                {
                    "answer": "Final revised answer.",
                    "reflection": {"missing": "None.", "superfluous": "None."},
                    "search_queries": ["cardiovascular breakfast pattern meta analysis"],
                    "references": ["https://example.com/ref-1"],
                },
            ),
            FakeResponse(
                "ReviseAnswer",
                {
                    "answer": "Final revised answer round 2.",
                    "reflection": {"missing": "None.", "superfluous": "None."},
                    "search_queries": ["glycemic load breakfast meta analysis"],
                    "references": ["https://example.com/ref-2"],
                },
            ),
            FakeResponse(
                "ReviseAnswer",
                {
                    "answer": "Final revised answer round 3.",
                    "reflection": {"missing": "None.", "superfluous": "None."},
                    "search_queries": ["protein breakfast insulin sensitivity trial"],
                    "references": ["https://example.com/ref-3"],
                },
            ),
        ]
    )
    workflow = build_external_reflection_graph(
        responder_chain=responder_chain,
        revisor_chain=revisor_chain,
        research_tool=FakeResearchTool(),
        max_iterations=3,
    )

    result = invoke_external_reflection_agent("question", workflow=workflow)

    assert result.initial_answer == "Initial answer."
    assert result.final_answer == "Final revised answer round 3."
    assert result.references == ("https://example.com/ref-3",)
    assert result.total_messages == 8
    assert "graph TD" in result.mermaid_graph


def test_external_research_tool_supports_empty_queries_without_error():
    tool = ExternalKnowledgeResearchTool(max_results=1, tavily_tool=None)

    assert tool.search("") == []


def test_select_best_available_ollama_model_prefers_ranked_candidate():
    selected_model = select_best_available_ollama_model(
        ["llama3.2:3b", "qwen2.5:7b", "mistral"],
    )

    assert selected_model == "qwen2.5:7b"