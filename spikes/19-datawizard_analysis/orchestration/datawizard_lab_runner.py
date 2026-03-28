# --- DEPENDENCIAS ---
from config.datawizard_config import BASELINE_QUERY
from config.datawizard_config import DATAWIZARD_INTRODUCTION
from config.datawizard_config import DEFAULT_DATAWIZARD_QUERIES
from models.datawizard_baseline_chat import answer_without_tools
from orchestration.datawizard_agent_orchestration import execute_datawizard_query
from orchestration.datawizard_tools_orchestration import describe_tool_schemas


def print_divider(title: str) -> None:
    print(f"\n=== {title} ===")


def run_datawizard_lab() -> None:
    print(DATAWIZARD_INTRODUCTION)
    print_divider("Tool Schema")
    for schema in describe_tool_schemas():
        print(schema["name"], "->", list(schema["args"].keys()))

    print_divider("Baseline Limitation")
    print(f"Query: {BASELINE_QUERY}")
    print(answer_without_tools(BASELINE_QUERY))

    print_divider("Executor Agent")
    for query in DEFAULT_DATAWIZARD_QUERIES:
        result = execute_datawizard_query(query)
        print(f"Query: {query}")
        for step in result.steps:
            print(f"  Tool: {step.tool_name} Args: {step.arguments} Result: {step.result}")
        print(f"  Final: {result.final_answer}")
