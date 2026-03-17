# --- DEPENDENCIAS ---
from config.interactive_agents_config import DEFAULT_AGENT_QUERIES
from config.interactive_agents_config import DEFAULT_MANUAL_TOOL_QUERY
from config.interactive_agents_config import DEFAULT_TIP_QUERY
from config.interactive_agents_config import LAB_INTRODUCTION
from orchestration.interactive_agents_agent_orchestration import TipAgent
from orchestration.interactive_agents_agent_orchestration import ToolCallingAgent
from orchestration.interactive_agents_manual_tool_calling_orchestration import (
    execute_manual_tool_calling_query,
)
from orchestration.interactive_agents_manual_tool_calling_orchestration import (
    summarize_manual_trace,
)
from orchestration.interactive_agents_tools_orchestration import add
from orchestration.interactive_agents_tools_orchestration import calculate_tip
from orchestration.interactive_agents_tools_orchestration import describe_tool_schemas


def print_divider(title: str) -> None:
    print(f"\n=== {title} ===")


def run_interactive_llm_agents_with_tools_lab() -> None:
    print(LAB_INTRODUCTION)

    print_divider("Tool Schema")
    for schema in describe_tool_schemas():
        print(schema["name"], "->", list(schema["args"].keys()))

    print_divider("Direct Tool Invocation")
    print("add:", add.invoke({"a": 1, "b": 2}))
    print(
        "calculate_tip:",
        calculate_tip.invoke({"total_bill": 120, "tip_percent": 15}),
    )

    print_divider("Manual Tool Calling")
    manual_result = execute_manual_tool_calling_query(DEFAULT_MANUAL_TOOL_QUERY)
    for line in summarize_manual_trace(manual_result):
        print(line)

    print_divider("Agent Examples")
    math_agent = ToolCallingAgent()
    for query in DEFAULT_AGENT_QUERIES:
        print(f"Query: {query}")
        print(f"Answer: {math_agent.run(query)}")

    print_divider("Tip Agent")
    tip_agent = TipAgent()
    print(f"Query: {DEFAULT_TIP_QUERY}")
    print(f"Answer: {tip_agent.run(DEFAULT_TIP_QUERY)}")
