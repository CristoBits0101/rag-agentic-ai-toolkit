# --- DEPENDENCIAS ---
from config.react_agent_config import DEFAULT_CALC_QUERY
from config.react_agent_config import DEFAULT_NEWS_QUERY
from config.react_agent_config import DEFAULT_WEATHER_QUERY
from config.react_agent_config import LAB_INTRODUCTION
from orchestration.react_agent_orchestration import build_react_workflow
from orchestration.react_agent_orchestration import invoke_react_query
from orchestration.react_tools_orchestration import describe_tool_schemas


def print_divider(title: str) -> None:
    print(f"\n=== {title} ===")


def print_tool_steps(result) -> None:
    for step in result.steps:
        print(f"Tool: {step.tool_name}")
        print(f"Arguments: {step.arguments}")
        print(f"Result: {step.result}")


def run_react_agent_lab() -> None:
    print(LAB_INTRODUCTION)
    print_divider("Tool Schemas")
    print(describe_tool_schemas())

    workflow = build_react_workflow()

    for title, query in (
        ("Weather and Clothing", DEFAULT_WEATHER_QUERY),
        ("Calculator Exercise", DEFAULT_CALC_QUERY),
        ("News Summary Exercise", DEFAULT_NEWS_QUERY),
    ):
        result = invoke_react_query(query, workflow=workflow)
        print_divider(title)
        print(f"Query: {result.query}")
        print_tool_steps(result)
        print(f"Final answer: {result.final_answer}")

    if result.mermaid_graph:
        print_divider("Mermaid Graph")
        print(result.mermaid_graph)