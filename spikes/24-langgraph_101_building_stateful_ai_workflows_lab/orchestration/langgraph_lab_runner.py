# --- DEPENDENCIAS ---
from config.langgraph_workflows_config import AUTH_DEMO_ATTEMPTS
from config.langgraph_workflows_config import AUTH_LOCKOUT_ATTEMPTS
from config.langgraph_workflows_config import COUNTER_INITIAL_STATE
from config.langgraph_workflows_config import LAB_INTRODUCTION
from config.langgraph_workflows_config import QA_SAMPLE_QUESTIONS
from models.langgraph_workflows_ollama_gateway import build_langgraph_ollama_chat_model
from orchestration.langgraph_auth_workflow import invoke_auth_workflow
from orchestration.langgraph_counter_workflow import invoke_counter_workflow
from orchestration.langgraph_qa_workflow import invoke_qa_workflow


def print_divider(title: str) -> None:
    print(f"\n=== {title} ===")


def run_authentication_demo() -> None:
    success_result = invoke_auth_workflow({"credential_attempts": AUTH_DEMO_ATTEMPTS})
    lockout_result = invoke_auth_workflow({"credential_attempts": AUTH_LOCKOUT_ATTEMPTS})

    print_divider("Authentication Workflow")
    print(f"Successful flow output: {success_result.output}")
    print(f"Successful flow attempts: {success_result.attempts}")
    print(f"Lockout flow output: {lockout_result.output}")
    print(f"Lockout flow attempts: {lockout_result.attempts}")


def run_qa_demo() -> None:
    print_divider("QA Workflow")

    try:
        model = build_langgraph_ollama_chat_model()
    except RuntimeError as exc:
        print(f"QA workflow skipped: {exc}")
        return

    for question in QA_SAMPLE_QUESTIONS:
        result = invoke_qa_workflow(question, model=model)
        print(f"Question: {result.question}")
        print(f"Answer: {result.answer}")


def run_counter_demo() -> None:
    print_divider("Counter Workflow")
    result = invoke_counter_workflow(COUNTER_INITIAL_STATE)
    print(f"Counter stopped at n={result.n} with letter={result.letter}")


def run_langgraph_lab() -> None:
    print(LAB_INTRODUCTION)
    run_authentication_demo()
    run_qa_demo()
    run_counter_demo()