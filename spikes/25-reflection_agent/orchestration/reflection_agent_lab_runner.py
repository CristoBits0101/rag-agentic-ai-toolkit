# --- DEPENDENCIAS ---
from config.reflection_agent_config import LAB_INTRODUCTION
from config.reflection_agent_config import SAMPLE_LINKEDIN_REQUEST
from models.reflection_agent_ollama_gateway import build_reflection_agent_ollama_chat_model
from orchestration.reflection_agent_workflow import build_reflection_agent_workflow
from orchestration.reflection_agent_workflow import invoke_reflection_agent


def print_divider(title: str) -> None:
    print(f"\n=== {title} ===")


def run_reflection_agent_lab() -> None:
    print(LAB_INTRODUCTION)

    try:
        model = build_reflection_agent_ollama_chat_model()
    except RuntimeError as exc:
        print(f"Reflection agent workflow skipped: {exc}")
        return

    workflow = build_reflection_agent_workflow(model=model)
    result = invoke_reflection_agent(SAMPLE_LINKEDIN_REQUEST, workflow=workflow)

    print_divider("Reflection Agent")
    print(f"Request: {result.request}")
    if result.generated_posts:
        print(f"First generated post: {result.generated_posts[0]}")
    if result.critiques:
        print(f"First critique: {result.critiques[0]}")
    print(f"Final post: {result.final_post}")
    print(f"Total messages in state: {result.total_messages}")

    if result.mermaid_graph:
        print_divider("Mermaid Graph")
        print(result.mermaid_graph)