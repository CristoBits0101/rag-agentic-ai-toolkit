# --- DEPENDENCIAS ---
import json
from typing import Any

from langchain_core.messages import AIMessage
from langchain_core.messages import HumanMessage
from langchain_core.messages import SystemMessage
from langchain_core.messages import ToolMessage
from langchain_core.tools import BaseTool

from config.interactive_agents_config import INTERACTIVE_TOOL_CALLING_SYSTEM_PROMPT
from config.interactive_agents_config import MAX_TOOL_AGENT_STEPS
from config.interactive_agents_config import TOOL_CALLING_RETRY_PROMPT
from models.interactive_agents_entities import InteractiveToolRunResult
from models.interactive_agents_entities import InteractiveToolStep
from models.interactive_agents_entities import ParsedToolCall
from models.interactive_agents_ollama_gateway import build_interactive_agents_ollama_chat_model
from orchestration.interactive_agents_tools_orchestration import build_interactive_tools
from orchestration.interactive_agents_tools_orchestration import build_tool_map
from orchestration.interactive_agents_tools_orchestration import normalize_tool_result


def query_requires_tools(query: str) -> bool:
    lowered_query = query.lower()
    arithmetic_markers = ["+", "-", "times", "multiply", "subtract", "add", "tip", "%"]
    return any(marker in lowered_query for marker in arithmetic_markers)


def extract_tool_calls_from_ai_message(ai_message: AIMessage) -> list[ParsedToolCall]:
    parsed_calls: list[ParsedToolCall] = []
    for tool_call in ai_message.tool_calls:
        parsed_calls.append(
            ParsedToolCall(
                tool_name=tool_call["name"],
                arguments=tool_call["args"],
                tool_call_id=tool_call["id"],
            )
        )

    return parsed_calls


def format_numeric_value(value: Any) -> str:
    if isinstance(value, int):
        return str(value)

    if isinstance(value, float):
        if float(value).is_integer():
            return str(int(value))
        return f"{value:.2f}".rstrip("0").rstrip(".")

    return str(value)


def build_safe_final_answer(model_answer: str, steps: list[InteractiveToolStep]) -> str:
    stripped_answer = model_answer.strip()
    if stripped_answer:
        return stripped_answer

    if not steps:
        return "No final answer was produced."

    last_result = steps[-1].result
    if "tip_amount" in last_result:
        return (
            "The tip amount is "
            f"{format_numeric_value(last_result['tip_amount'])} and the total with tip is "
            f"{format_numeric_value(last_result['total_with_tip'])}."
        )

    if "result" in last_result:
        return f"The final result is {format_numeric_value(last_result['result'])}."

    return json.dumps(last_result, ensure_ascii=True)


def build_tool_message_content(result: dict[str, Any]) -> str:
    return json.dumps(result, ensure_ascii=True)


def execute_parsed_tool_calls(
    parsed_tool_calls: list[ParsedToolCall],
    tool_map: dict[str, BaseTool],
) -> tuple[list[InteractiveToolStep], list[ToolMessage]]:
    steps: list[InteractiveToolStep] = []
    tool_messages: list[ToolMessage] = []

    for parsed_tool_call in parsed_tool_calls:
        if parsed_tool_call.tool_name not in tool_map:
            raise KeyError(f"Tool {parsed_tool_call.tool_name} is not registered.")

        tool = tool_map[parsed_tool_call.tool_name]
        normalized_result = normalize_tool_result(tool.invoke(parsed_tool_call.arguments))
        steps.append(
            InteractiveToolStep(
                tool_name=parsed_tool_call.tool_name,
                arguments=parsed_tool_call.arguments,
                result=normalized_result,
            )
        )
        tool_messages.append(
            ToolMessage(
                content=build_tool_message_content(normalized_result),
                tool_call_id=parsed_tool_call.tool_call_id,
                name=parsed_tool_call.tool_name,
            )
        )

    return steps, tool_messages


def looks_like_tool_retry_message(message: Any) -> bool:
    return isinstance(message, HumanMessage) and TOOL_CALLING_RETRY_PROMPT in str(message.content)


def execute_manual_tool_calling_query(
    query: str,
    tools: list[BaseTool] | None = None,
    model=None,
    max_steps: int = MAX_TOOL_AGENT_STEPS,
) -> InteractiveToolRunResult:
    selected_tools = tools or build_interactive_tools()
    selected_model = model or build_interactive_agents_ollama_chat_model()
    bound_model = selected_model.bind_tools(selected_tools)
    tool_map = build_tool_map(selected_tools)
    messages = [
        SystemMessage(content=INTERACTIVE_TOOL_CALLING_SYSTEM_PROMPT),
        HumanMessage(content=query),
    ]
    collected_tool_calls: list[ParsedToolCall] = []
    collected_steps: list[InteractiveToolStep] = []

    for _ in range(max_steps):
        ai_message = bound_model.invoke(messages)
        messages.append(ai_message)
        parsed_tool_calls = extract_tool_calls_from_ai_message(ai_message)

        if not parsed_tool_calls:
            if not collected_steps and query_requires_tools(query) and not any(
                looks_like_tool_retry_message(message) for message in messages
            ):
                messages.append(HumanMessage(content=TOOL_CALLING_RETRY_PROMPT))
                continue

            return InteractiveToolRunResult(
                query=query,
                final_answer=build_safe_final_answer(str(ai_message.content), collected_steps),
                tool_calls=collected_tool_calls,
                steps=collected_steps,
                messages=messages,
            )

        collected_tool_calls.extend(parsed_tool_calls)
        step_batch, tool_messages = execute_parsed_tool_calls(parsed_tool_calls, tool_map)
        collected_steps.extend(step_batch)
        messages.extend(tool_messages)

    raise RuntimeError(f"Tool calling loop exceeded {max_steps} steps for query: {query}")


def summarize_manual_trace(result: InteractiveToolRunResult) -> list[str]:
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
