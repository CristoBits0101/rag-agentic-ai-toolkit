# --- DEPENDENCIAS ---
import json
from typing import Any

from langchain_core.messages import AIMessage
from langchain_core.messages import HumanMessage
from langchain_core.messages import SystemMessage
from langchain_core.messages import ToolMessage
from langchain_core.runnables import RunnableLambda
from langchain_core.runnables import RunnablePassthrough
from langchain_core.tools import BaseTool

from config.youtube_tool_calling_agent_config import FIXED_CHAIN_QUERY
from config.youtube_tool_calling_agent_config import MAX_RECURSIVE_TOOL_ITERATIONS
from config.youtube_tool_calling_agent_config import YOUTUBE_TOOL_RETRY_PROMPT
from config.youtube_tool_calling_agent_config import YOUTUBE_TOOL_SYSTEM_PROMPT
from models.youtube_tool_calling_entities import YouTubeParsedToolCall
from models.youtube_tool_calling_entities import YouTubeToolRunResult
from models.youtube_tool_calling_entities import YouTubeToolStep
from models.youtube_tool_calling_ollama_gateway import build_youtube_tool_calling_ollama_chat_model
from orchestration.youtube_tool_calling_tools_orchestration import build_tool_mapping
from orchestration.youtube_tool_calling_tools_orchestration import build_youtube_agent_tools


def serialize_tool_result(result: Any) -> str:
    if isinstance(result, (dict, list)):
        return json.dumps(result, ensure_ascii=True)

    return str(result)


def query_requires_youtube_tools(query: str) -> bool:
    lowered_query = query.lower()
    youtube_markers = [
        "youtube",
        "youtu.be",
        "video",
        "transcript",
        "thumbnail",
        "metadata",
        "search",
        "summary",
    ]
    return any(marker in lowered_query for marker in youtube_markers)


def extract_tool_calls_from_ai_message(ai_message: AIMessage) -> list[YouTubeParsedToolCall]:
    parsed_tool_calls: list[YouTubeParsedToolCall] = []
    for tool_call in ai_message.tool_calls:
        parsed_tool_calls.append(
            YouTubeParsedToolCall(
                tool_name=tool_call["name"],
                arguments=tool_call["args"],
                tool_call_id=tool_call["id"],
            )
        )

    return parsed_tool_calls


def build_safe_final_answer(model_answer: str, steps: list[YouTubeToolStep]) -> str:
    stripped_answer = model_answer.strip()
    if stripped_answer:
        return stripped_answer

    if not steps:
        return "No final answer was produced."

    last_result = steps[-1].result
    if isinstance(last_result, (dict, list)):
        return json.dumps(last_result, ensure_ascii=True)

    return str(last_result)


def execute_tool(tool_call: dict[str, Any], tool_mapping: dict[str, BaseTool]) -> ToolMessage:
    if tool_call["name"] not in tool_mapping:
        raise KeyError(f"Tool {tool_call['name']} is not registered.")

    tool = tool_mapping[tool_call["name"]]
    result = tool.invoke(tool_call["args"])
    return ToolMessage(
        content=serialize_tool_result(result),
        tool_call_id=tool_call["id"],
        name=tool_call["name"],
    )


def execute_tool_and_capture_step(
    tool_call: dict[str, Any],
    tool_mapping: dict[str, BaseTool],
) -> tuple[YouTubeToolStep, ToolMessage]:
    tool_message = execute_tool(tool_call, tool_mapping)
    parsed_content: Any = tool_message.content

    try:
        parsed_content = json.loads(str(tool_message.content))
    except Exception:
        parsed_content = str(tool_message.content)

    return (
        YouTubeToolStep(
            tool_name=tool_call["name"],
            arguments=tool_call["args"],
            result=parsed_content,
        ),
        tool_message,
    )


def execute_tool_batch(
    tool_calls: list[dict[str, Any]],
    tool_mapping: dict[str, BaseTool],
) -> tuple[list[YouTubeToolStep], list[ToolMessage]]:
    steps: list[YouTubeToolStep] = []
    tool_messages: list[ToolMessage] = []

    for tool_call in tool_calls:
        step, tool_message = execute_tool_and_capture_step(tool_call, tool_mapping)
        steps.append(step)
        tool_messages.append(tool_message)

    return steps, tool_messages


def needs_tool_retry(messages: list[Any], query: str) -> bool:
    if not query_requires_youtube_tools(query):
        return False

    return not any(
        isinstance(message, HumanMessage) and YOUTUBE_TOOL_RETRY_PROMPT in str(message.content)
        for message in messages
    )


def request_ai_response(
    messages: list[Any],
    llm_with_tools,
    query: str,
) -> tuple[AIMessage, list[Any]]:
    ai_response = llm_with_tools.invoke(messages)
    if ai_response.tool_calls or not needs_tool_retry(messages, query):
        return ai_response, messages

    retried_messages = messages + [HumanMessage(content=YOUTUBE_TOOL_RETRY_PROMPT)]
    retry_response = llm_with_tools.invoke(retried_messages)
    if retry_response.tool_calls:
        return retry_response, retried_messages

    return ai_response, messages


def request_final_answer(
    messages: list[Any],
    llm_with_tools,
    query: str,
) -> tuple[AIMessage, list[Any]]:
    final_response, messages = request_ai_response(messages, llm_with_tools, query)
    if final_response.tool_calls or str(final_response.content).strip():
        return final_response, messages

    follow_up_messages = messages + [
        HumanMessage(content="Provide the final answer now using the gathered YouTube data.")
    ]
    follow_up_response = llm_with_tools.invoke(follow_up_messages)
    return follow_up_response, follow_up_messages


def execute_manual_youtube_summary_flow(
    query: str = FIXED_CHAIN_QUERY,
    tools: list[BaseTool] | None = None,
    model=None,
) -> YouTubeToolRunResult:
    selected_tools = tools or build_youtube_agent_tools()
    selected_model = model or build_youtube_tool_calling_ollama_chat_model()
    llm_with_tools = selected_model.bind_tools(selected_tools)
    tool_mapping = build_tool_mapping(selected_tools)
    messages: list[Any] = [
        SystemMessage(content=YOUTUBE_TOOL_SYSTEM_PROMPT),
        HumanMessage(content=query),
    ]
    collected_tool_calls: list[YouTubeParsedToolCall] = []
    collected_steps: list[YouTubeToolStep] = []

    first_response, messages = request_ai_response(messages, llm_with_tools, query)
    messages.append(first_response)
    first_tool_calls = extract_tool_calls_from_ai_message(first_response)
    if not first_tool_calls:
        return YouTubeToolRunResult(
            query=query,
            final_answer=build_safe_final_answer(str(first_response.content), collected_steps),
            tool_calls=collected_tool_calls,
            steps=collected_steps,
            messages=messages,
        )

    collected_tool_calls.extend(first_tool_calls)
    first_steps, first_tool_messages = execute_tool_batch(first_response.tool_calls, tool_mapping)
    collected_steps.extend(first_steps)
    messages.extend(first_tool_messages)

    second_response, messages = request_ai_response(messages, llm_with_tools, query)
    messages.append(second_response)
    second_tool_calls = extract_tool_calls_from_ai_message(second_response)
    if not second_tool_calls:
        return YouTubeToolRunResult(
            query=query,
            final_answer=build_safe_final_answer(str(second_response.content), collected_steps),
            tool_calls=collected_tool_calls,
            steps=collected_steps,
            messages=messages,
        )

    collected_tool_calls.extend(second_tool_calls)
    second_steps, second_tool_messages = execute_tool_batch(second_response.tool_calls, tool_mapping)
    collected_steps.extend(second_steps)
    messages.extend(second_tool_messages)

    final_response, messages = request_final_answer(messages, llm_with_tools, query)
    messages.append(final_response)

    return YouTubeToolRunResult(
        query=query,
        final_answer=build_safe_final_answer(str(final_response.content), collected_steps),
        tool_calls=collected_tool_calls,
        steps=collected_steps,
        messages=messages,
    )


def invoke_fixed_chain_summary(state: dict[str, Any], llm_with_tools) -> str:
    second_response = state["ai_response2"]
    if not second_response.tool_calls and str(second_response.content).strip():
        return str(second_response.content).strip()

    return str(llm_with_tools.invoke(state["messages"]).content).strip()


def build_fixed_summarization_chain(model=None, tools: list[BaseTool] | None = None):
    selected_tools = tools or build_youtube_agent_tools()
    selected_model = model or build_youtube_tool_calling_ollama_chat_model()
    llm_with_tools = selected_model.bind_tools(selected_tools)
    tool_mapping = build_tool_mapping(selected_tools)

    initial_setup = RunnablePassthrough.assign(
        messages=lambda x: [
            SystemMessage(content=YOUTUBE_TOOL_SYSTEM_PROMPT),
            HumanMessage(content=x["query"]),
        ]
    )
    first_llm_call = RunnablePassthrough.assign(
        ai_response=lambda x: llm_with_tools.invoke(x["messages"])
    )
    first_tool_processing = RunnablePassthrough.assign(
        tool_messages=lambda x: [
            execute_tool(tool_call, tool_mapping) for tool_call in x["ai_response"].tool_calls
        ]
    ).assign(
        messages=lambda x: x["messages"] + [x["ai_response"]] + x["tool_messages"]
    )
    second_llm_call = RunnablePassthrough.assign(
        ai_response2=lambda x: llm_with_tools.invoke(x["messages"])
    )
    second_tool_processing = RunnablePassthrough.assign(
        tool_messages2=lambda x: [
            execute_tool(tool_call, tool_mapping) for tool_call in x["ai_response2"].tool_calls
        ]
    ).assign(
        messages=lambda x: x["messages"] + [x["ai_response2"]] + x["tool_messages2"]
    )
    final_summary = RunnablePassthrough.assign(
        summary=lambda x: invoke_fixed_chain_summary(x, llm_with_tools)
    ) | RunnableLambda(lambda x: x["summary"])

    return (
        initial_setup
        | first_llm_call
        | first_tool_processing
        | second_llm_call
        | second_tool_processing
        | final_summary
    )


def process_tool_calls(
    messages: list[Any],
    llm_with_tools,
    tool_mapping: dict[str, BaseTool],
    query: str,
) -> list[Any]:
    last_message = messages[-1]
    tool_messages = [
        execute_tool(tool_call, tool_mapping) for tool_call in getattr(last_message, "tool_calls", [])
    ]
    updated_messages = messages + tool_messages
    next_response, updated_messages = request_ai_response(updated_messages, llm_with_tools, query)
    return updated_messages + [next_response]


def should_continue(messages: list[Any]) -> bool:
    last_message = messages[-1]
    return bool(getattr(last_message, "tool_calls", None))


def recursive_chain_runner(
    messages: list[Any],
    llm_with_tools,
    tool_mapping: dict[str, BaseTool],
    query: str,
    remaining_iterations: int = MAX_RECURSIVE_TOOL_ITERATIONS,
) -> list[Any]:
    if remaining_iterations <= 0 or not should_continue(messages):
        return messages

    updated_messages = process_tool_calls(messages, llm_with_tools, tool_mapping, query)
    return recursive_chain_runner(
        updated_messages,
        llm_with_tools,
        tool_mapping,
        query,
        remaining_iterations - 1,
    )


def build_universal_recursive_chain(model=None, tools: list[BaseTool] | None = None):
    selected_tools = tools or build_youtube_agent_tools()
    selected_model = model or build_youtube_tool_calling_ollama_chat_model()
    llm_with_tools = selected_model.bind_tools(selected_tools)
    tool_mapping = build_tool_mapping(selected_tools)

    def get_latest_human_content(messages: list[Any]) -> str:
        for message in reversed(messages):
            if isinstance(message, HumanMessage):
                return str(message.content)

        return ""

    def initial_model_step(messages: list[Any]) -> list[Any]:
        query = get_latest_human_content(messages)
        ai_response, updated_messages = request_ai_response(messages, llm_with_tools, query)
        return updated_messages + [ai_response]

    return (
        RunnableLambda(
            lambda x: [
                SystemMessage(content=YOUTUBE_TOOL_SYSTEM_PROMPT),
                HumanMessage(content=x["query"]),
            ]
        )
        | RunnableLambda(initial_model_step)
        | RunnableLambda(
            lambda messages: recursive_chain_runner(
                messages,
                llm_with_tools,
                tool_mapping,
                get_latest_human_content(messages),
            )
        )
    )


def extract_final_response_content(messages: list[Any]) -> str:
    last_message = messages[-1]
    last_content = str(getattr(last_message, "content", "")).strip()
    if last_content:
        return last_content

    for message in reversed(messages):
        message_content = str(getattr(message, "content", "")).strip()
        if message_content:
            return message_content

    return "No final answer was produced."


class YouTubeToolCallingAgent:
    def __init__(self, model=None, tools: list[BaseTool] | None = None):
        self._chain = build_universal_recursive_chain(model=model, tools=tools)

    def run(self, query: str) -> str:
        messages = self._chain.invoke({"query": query})
        return extract_final_response_content(messages)


def summarize_manual_trace(result: YouTubeToolRunResult) -> list[str]:
    trace_lines = [f"Query: {result.query}"]
    for tool_call in result.tool_calls:
        trace_lines.append(
            f"Tool call: {tool_call.tool_name} Args: {tool_call.arguments} Id: {tool_call.tool_call_id}"
        )
    for step in result.steps:
        trace_lines.append(
            f"Tool result: {step.tool_name} Args: {step.arguments} Result: {step.result}"
        )
    trace_lines.append(f"Final answer: {result.final_answer}")
    return trace_lines
