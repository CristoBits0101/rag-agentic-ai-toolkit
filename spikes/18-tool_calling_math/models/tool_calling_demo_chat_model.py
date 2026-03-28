# --- DEPENDENCIAS ---
import json
from typing import Any

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage
from langchain_core.messages import BaseMessage
from langchain_core.messages import HumanMessage
from langchain_core.messages import ToolMessage
from langchain_core.messages.tool import tool_call
from langchain_core.outputs import ChatGeneration
from langchain_core.outputs import ChatResult
from langchain_core.runnables import RunnableLambda
from langchain_core.tools import BaseTool

from orchestration.tool_calling_tools_orchestration import extract_numbers_from_text

def normalize_query_text(text: str) -> str:
    return " ".join(text.lower().split())


def extract_numeric_literals(text: str) -> list[str]:
    return [
        format_numeric_answer(value)
        for value in extract_numbers_from_text(text)
    ]


def parse_tool_message_content(message: ToolMessage) -> dict[str, Any]:
    try:
        return json.loads(message.content)
    except json.JSONDecodeError:
        return {"result": message.content}


def format_numeric_answer(value: Any) -> str:
    if isinstance(value, int):
        return str(value)

    if isinstance(value, float):
        if value.is_integer():
            return str(int(value))
        return f"{value:.6f}".rstrip("0").rstrip(".")

    return str(value)


def build_tool_call_message(tool_name: str, arguments: dict[str, Any], call_id: str) -> AIMessage:
    return AIMessage(
        content="",
        tool_calls=[
            tool_call(
                name=tool_name,
                args=arguments,
                id=call_id,
            )
        ],
    )


def find_original_query(messages: list[BaseMessage]) -> str:
    for message in messages:
        if isinstance(message, HumanMessage):
            return str(message.content)

    return ""


def extract_tool_messages(messages: list[BaseMessage]) -> list[ToolMessage]:
    return [message for message in messages if isinstance(message, ToolMessage)]


def build_initial_tool_message(query: str) -> AIMessage:
    normalized_query = normalize_query_text(query)
    numeric_literals = extract_numeric_literals(normalized_query)

    if "population of canada" in normalized_query:
        return build_tool_call_message(
            "search_local_reference_fact",
            {"query": "population of canada"},
            "call_fact_1",
        )

    if "power" in normalized_query or "raised to" in normalized_query:
        return build_tool_call_message(
            "calculate_power",
            {"inputs": " ".join(numeric_literals[:2])},
            "call_power_1",
        )

    if "divide" in normalized_query or "divided by" in normalized_query:
        return build_tool_call_message(
            "divide_numbers",
            {"inputs": " ".join(numeric_literals)},
            "call_divide_1",
        )

    if "subtract" in normalized_query:
        if " from " in normalized_query and len(numeric_literals) >= 2:
            ordered_literals = [numeric_literals[1], numeric_literals[0], *numeric_literals[2:]]
            return build_tool_call_message(
                "subtract_numbers",
                {"inputs": " ".join(ordered_literals)},
                "call_subtract_1",
            )

        return build_tool_call_message(
            "subtract_numbers",
            {"inputs": " ".join(numeric_literals)},
            "call_subtract_1",
        )

    if "then multiply" in normalized_query:
        return build_tool_call_message(
            "add_numbers",
            {"inputs": " ".join(numeric_literals[:2])},
            "call_add_1",
        )

    if "multiply" in normalized_query:
        return build_tool_call_message(
            "multiply_numbers",
            {"inputs": " ".join(numeric_literals)},
            "call_multiply_1",
        )

    if "add" in normalized_query or "sum" in normalized_query:
        return build_tool_call_message(
            "add_numbers",
            {"inputs": " ".join(numeric_literals)},
            "call_add_1",
        )

    return AIMessage(
        content=(
            "I can help with arithmetic and local fact lookup. "
            "Try an addition subtraction multiplication division power or fact query."
        )
    )


def build_follow_up_tool_message(
    query: str,
    tool_messages: list[ToolMessage],
) -> AIMessage | None:
    normalized_query = normalize_query_text(query)
    last_payload = parse_tool_message_content(tool_messages[-1])
    numeric_literals = extract_numeric_literals(normalized_query)

    if "then multiply" in normalized_query and tool_messages[-1].name == "add_numbers":
        if len(numeric_literals) >= 3:
            first_result = format_numeric_answer(last_payload["result"])
            return build_tool_call_message(
                "multiply_numbers",
                {"inputs": f"{first_result} {numeric_literals[-1]}"},
                "call_multiply_2",
            )

    if "population of canada" in normalized_query and tool_messages[-1].name == "search_local_reference_fact":
        if numeric_literals:
            first_result = format_numeric_answer(last_payload["result"])
            return build_tool_call_message(
                "multiply_numbers",
                {"inputs": f"{first_result} {numeric_literals[-1]}"},
                "call_multiply_2",
            )

    return None


def build_final_message(query: str, tool_messages: list[ToolMessage]) -> AIMessage:
    last_payload = parse_tool_message_content(tool_messages[-1])
    result_value = last_payload.get("result")
    formatted_result = format_numeric_answer(result_value)
    normalized_query = normalize_query_text(query)

    if "population of canada" in normalized_query:
        return AIMessage(
            content=(
                "Using the local reference fact and the requested multiplier the final result is "
                f"{formatted_result}."
            )
        )

    return AIMessage(content=f"The final result is {formatted_result}.")


def coerce_messages_input(messages_input: Any) -> list[BaseMessage]:
    if isinstance(messages_input, dict) and "messages" in messages_input:
        return messages_input["messages"]

    return messages_input


class ToolCallingMathDemoChatModel(BaseChatModel):
    @property
    def _llm_type(self) -> str:
        return "tool_calling_math_demo_chat_model"

    @property
    def _identifying_params(self) -> dict[str, str]:
        return {"model_name": "tool_calling_math_demo_chat_model"}

    def _generate(
        self,
        messages: list[BaseMessage],
        stop: list[str] | None = None,
        run_manager=None,
        **kwargs,
    ) -> ChatResult:
        response = self.build_response(messages, {})
        return ChatResult(generations=[ChatGeneration(message=response)])

    def bind_tools(
        self,
        tools: list[dict[str, Any] | type | Any | BaseTool],
        *,
        tool_choice: str | None = None,
        **kwargs: Any,
    ):
        tool_map = {
            tool.name: tool
            for tool in tools
            if hasattr(tool, "name")
        }
        return RunnableLambda(
            lambda messages_input: self.build_response(
                coerce_messages_input(messages_input),
                tool_map,
            )
        )

    def build_response(
        self,
        messages: list[BaseMessage],
        tool_map: dict[str, BaseTool],
    ) -> AIMessage:
        query = find_original_query(messages)
        tool_messages = extract_tool_messages(messages)

        if not tool_map or not tool_messages:
            return build_initial_tool_message(query)

        follow_up_message = build_follow_up_tool_message(query, tool_messages)
        if follow_up_message is not None:
            return follow_up_message

        return build_final_message(query, tool_messages)


def build_tool_calling_math_demo_chat_model() -> ToolCallingMathDemoChatModel:
    return ToolCallingMathDemoChatModel()
