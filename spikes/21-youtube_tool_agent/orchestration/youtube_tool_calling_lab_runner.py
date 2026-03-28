# --- DEPENDENCIAS ---
from config.youtube_tool_calling_agent_config import DIRECT_SEARCH_QUERY
from config.youtube_tool_calling_agent_config import FIXED_CHAIN_QUERY
from config.youtube_tool_calling_agent_config import LAB_INTRODUCTION
from config.youtube_tool_calling_agent_config import SAMPLE_VIDEO_URL
from config.youtube_tool_calling_agent_config import UNIVERSAL_CHAIN_QUERY
from orchestration.youtube_tool_calling_agent_orchestration import (
    YouTubeToolCallingAgent,
)
from orchestration.youtube_tool_calling_agent_orchestration import (
    build_fixed_summarization_chain,
)
from orchestration.youtube_tool_calling_agent_orchestration import (
    execute_manual_youtube_summary_flow,
)
from orchestration.youtube_tool_calling_agent_orchestration import (
    summarize_manual_trace,
)
from orchestration.youtube_tool_calling_tools_orchestration import describe_tool_schemas
from orchestration.youtube_tool_calling_tools_orchestration import extract_video_id
from orchestration.youtube_tool_calling_tools_orchestration import search_youtube


def print_divider(title: str) -> None:
    print(f"\n=== {title} ===")


def run_youtube_tool_calling_agent_lab() -> None:
    print(LAB_INTRODUCTION)

    print_divider("Tool Schema")
    for schema in describe_tool_schemas():
        print(schema["name"], "->", list(schema["args"].keys()))

    print_divider("Direct Tool Invocation")
    print("extract_video_id:", extract_video_id.invoke({"url": SAMPLE_VIDEO_URL}))
    search_results = search_youtube.invoke({"query": DIRECT_SEARCH_QUERY, "limit": 2})
    print("search_youtube:", search_results[:2] if isinstance(search_results, list) else search_results)

    print_divider("Manual Tool Calling")
    manual_result = execute_manual_youtube_summary_flow(FIXED_CHAIN_QUERY)
    for line in summarize_manual_trace(manual_result):
        print(line)

    print_divider("Fixed Summarization Chain")
    fixed_chain = build_fixed_summarization_chain()
    fixed_summary = fixed_chain.invoke({"query": FIXED_CHAIN_QUERY})
    print(fixed_summary)

    print_divider("Universal Recursive Agent")
    agent = YouTubeToolCallingAgent()
    print(agent.run(UNIVERSAL_CHAIN_QUERY))
