# --- DEPENDENCIAS ---
from config.external_reflection_agent_config import LAB_INTRODUCTION
from config.external_reflection_agent_config import SAMPLE_QUESTION
from models.external_knowledge_gateway import ExternalKnowledgeResearchTool
from models.external_reflection_ollama_gateway import build_external_reflection_ollama_chat_model
from orchestration.external_reflection_agent_workflow import build_external_reflection_graph
from orchestration.external_reflection_agent_workflow import invoke_external_reflection_agent


def print_divider(title: str) -> None:
    print(f"\n=== {title} ===")


def run_external_reflection_agent_lab() -> None:
    print(LAB_INTRODUCTION)

    try:
        model = build_external_reflection_ollama_chat_model()
    except RuntimeError as exc:
        print(f"External reflection workflow skipped: {exc}")
        return

    research_tool = ExternalKnowledgeResearchTool()
    workflow = build_external_reflection_graph(model=model, research_tool=research_tool)
    result = invoke_external_reflection_agent(SAMPLE_QUESTION, workflow=workflow)

    print_divider("External Reflection Agent")
    print(f"Question: {result.question}")
    print(f"Initial answer: {result.initial_answer}")
    print(f"Final answer: {result.final_answer}")
    print(f"Search queries: {result.search_queries}")
    print(f"References: {result.references}")
    print(f"Total messages in state: {result.total_messages}")

    if result.mermaid_graph:
        print_divider("Mermaid Graph")
        print(result.mermaid_graph)