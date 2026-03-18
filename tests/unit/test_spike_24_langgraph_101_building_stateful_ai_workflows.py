# --- DEPENDENCIAS ---
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPIKE = ROOT / "spikes" / "24-langgraph_101_building_stateful_ai_workflows_lab"

if str(SPIKE) not in sys.path:
    sys.path.insert(0, str(SPIKE))

from config.langgraph_workflows_config import AUTH_DEMO_ATTEMPTS
from config.langgraph_workflows_config import AUTH_LOCKOUT_ATTEMPTS
from config.langgraph_workflows_config import LANGGRAPH_GUIDED_PROJECT_CONTEXT
from models.langgraph_workflows_ollama_gateway import select_best_available_ollama_model
from orchestration.langgraph_auth_workflow import auth_router
from orchestration.langgraph_auth_workflow import input_node
from orchestration.langgraph_auth_workflow import invoke_auth_workflow
from orchestration.langgraph_auth_workflow import validate_credentials_node
from orchestration.langgraph_counter_workflow import add
from orchestration.langgraph_counter_workflow import invoke_counter_workflow
from orchestration.langgraph_counter_workflow import stop_condition
from orchestration.langgraph_qa_workflow import build_qa_prompt
from orchestration.langgraph_qa_workflow import context_provider_node
from orchestration.langgraph_qa_workflow import input_validation_node
from orchestration.langgraph_qa_workflow import invoke_qa_workflow
from orchestration.langgraph_qa_workflow import llm_qa_node


class FakeResponse:
    def __init__(self, content: str):
        self.content = content


class FakeModel:
    def __init__(self, content: str):
        self.content = content
        self.prompts: list[str] = []

    def invoke(self, prompt: str):
        self.prompts.append(prompt)
        return FakeResponse(self.content)


def test_input_node_reads_next_credential_attempt():
    state = {
        "credential_attempts": AUTH_DEMO_ATTEMPTS,
        "attempt_index": 0,
    }

    result = input_node(state)

    assert result == {
        "username": "test_user",
        "password": "wrongpassword",
        "attempt_index": 1,
    }


def test_validate_credentials_node_marks_success_for_valid_credentials():
    result = validate_credentials_node(
        {
            "username": "test_user",
            "password": "secure_password",
            "attempts": 0,
        }
    )

    assert result == {"is_authenticated": True, "attempts": 1}


def test_auth_router_retries_when_more_attempts_are_available():
    decision = auth_router(
        {
            "is_authenticated": False,
            "attempt_index": 1,
            "attempts": 1,
            "credential_attempts": AUTH_DEMO_ATTEMPTS,
            "max_attempts": 3,
        }
    )

    assert decision == "retry"


def test_invoke_auth_workflow_succeeds_after_retry():
    result = invoke_auth_workflow({"credential_attempts": AUTH_DEMO_ATTEMPTS})

    assert result.is_authenticated is True
    assert result.attempts == 2
    assert result.output == "Authentication successful! Welcome."


def test_invoke_auth_workflow_locks_after_max_attempts():
    result = invoke_auth_workflow({"credential_attempts": AUTH_LOCKOUT_ATTEMPTS})

    assert result.is_authenticated is False
    assert result.attempts == 3
    assert result.output == "Authentication failed after 3 attempt(s)."


def test_input_validation_node_rejects_empty_question():
    result = input_validation_node({"question": "   "})

    assert result == {
        "valid": False,
        "error": "Question cannot be empty.",
    }


def test_context_provider_node_returns_langgraph_context_for_relevant_question():
    result = context_provider_node({"question": "What is LangGraph?"})

    assert result == {"context": LANGGRAPH_GUIDED_PROJECT_CONTEXT}


def test_build_qa_prompt_includes_context_and_question():
    prompt = build_qa_prompt("What is LangGraph?", LANGGRAPH_GUIDED_PROJECT_CONTEXT)

    assert "What is LangGraph?" in prompt
    assert LANGGRAPH_GUIDED_PROJECT_CONTEXT in prompt


def test_llm_qa_node_uses_model_when_context_exists():
    fake_model = FakeModel("LangGraph is a framework for stateful workflows.")

    result = llm_qa_node(
        {
            "question": "What is LangGraph?",
            "context": LANGGRAPH_GUIDED_PROJECT_CONTEXT,
        },
        model=fake_model,
    )

    assert result == {"answer": "LangGraph is a framework for stateful workflows."}
    assert fake_model.prompts


def test_invoke_qa_workflow_returns_fallback_for_irrelevant_question():
    fake_model = FakeModel("unused")

    result = invoke_qa_workflow("What is the weather today?", model=fake_model)

    assert result.valid is True
    assert result.context is None
    assert result.answer == (
        "I don't have enough context to answer your question. "
        "Please ask about the guided project."
    )


def test_add_increments_counter_and_updates_letter():
    result = add({"n": 1, "letter": ""}, letter_picker=lambda: "z")

    assert result == {"n": 2, "letter": "z"}


def test_stop_condition_ends_when_counter_reaches_thirteen():
    assert stop_condition({"n": 13, "letter": "a"}) is True
    assert stop_condition({"n": 12, "letter": "a"}) is False


def test_invoke_counter_workflow_runs_until_thirteen():
    result = invoke_counter_workflow({"n": 1, "letter": ""}, letter_picker=lambda: "x")

    assert result.n == 13
    assert result.letter == "x"


def test_select_best_available_ollama_model_prefers_ranked_candidate():
    selected_model = select_best_available_ollama_model(
        ["llama3.2:3b", "qwen2.5:7b", "mistral"],
    )

    assert selected_model == "qwen2.5:7b"