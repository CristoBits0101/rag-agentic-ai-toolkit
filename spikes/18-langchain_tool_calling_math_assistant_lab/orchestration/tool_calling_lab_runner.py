# --- DEPENDENCIAS ---
from config.tool_calling_math_config import DEFAULT_TOOL_CALLING_QUERIES
from config.tool_calling_math_config import DEMO_INTRODUCTION
from orchestration.tool_calling_agent_orchestration import execute_tool_calling_query
from orchestration.tool_calling_tools_orchestration import add_numbers
from orchestration.tool_calling_tools_orchestration import build_math_assistant_tools
from orchestration.tool_calling_tools_orchestration import describe_tool_schemas


def print_divider(title: str) -> None:
    print(f"\n=== {title} ===")


def run_langchain_tool_calling_math_assistant_lab() -> None:
    print(DEMO_INTRODUCTION)
    print_divider("Tool Schema")
    for schema in describe_tool_schemas(build_math_assistant_tools()):
        print(schema["name"], "->", list(schema["args"].keys()))

    print_divider("Direct Tool Invocation")
    print(add_numbers.invoke({"inputs": "Add 10, 20, two and 30"}))

    print_divider("Tool Calling Queries")
    for query in DEFAULT_TOOL_CALLING_QUERIES:
        result = execute_tool_calling_query(query)
        print(f"Query: {query}")
        for step in result.steps:
            print(f"  Tool: {step.tool_name} Args: {step.arguments} Result: {step.result}")
        print(f"  Final: {result.final_answer}")
