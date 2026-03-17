# --- DEPENDENCIAS ---
import json
from typing import Any

from langchain_core.messages import HumanMessage
from langchain_core.messages import ToolMessage
from langchain_core.tools import BaseTool

from config.tool_calling_math_config import MAX_TOOL_CALLING_STEPS
from models.tool_calling_demo_chat_model import (
    build_tool_calling_math_demo_chat_model,
)
from models.tool_calling_math_entities import ToolCallingRunResult
from models.tool_calling_math_entities import ToolCallingStep
from orchestration.tool_calling_tools_orchestration import build_math_assistant_tools


def normalize_tool_result(raw_result: Any) -> dict[str, Any]:
    if isinstance(raw_result, dict):
        return raw_result

    return {"result": raw_result}


def execute_tool_calling_query(
    query: str,
    tools: list[BaseTool] | None = None,
    model=None,
    max_steps: int = MAX_TOOL_CALLING_STEPS,
) -> ToolCallingRunResult:
    selected_tools = tools or build_math_assistant_tools()
    selected_model = model or build_tool_calling_math_demo_chat_model()
    bound_model = selected_model.bind_tools(selected_tools)
    tool_map = {tool.name: tool for tool in selected_tools}
    messages = [HumanMessage(content=query)]
    steps: list[ToolCallingStep] = []

    for _ in range(max_steps):
        ai_message = bound_model.invoke(messages)
        messages.append(ai_message)

        if not ai_message.tool_calls:
            return ToolCallingRunResult(
                query=query,
                final_answer=str(ai_message.content),
                steps=steps,
                messages=messages,
            )

        for tool_call_payload in ai_message.tool_calls:
            tool_name = tool_call_payload["name"]
            if tool_name not in tool_map:
                raise KeyError(f"Tool {tool_name} is not registered.")

            tool = tool_map[tool_name]
            tool_result = normalize_tool_result(tool.invoke(tool_call_payload["args"]))
            steps.append(
                ToolCallingStep(
                    tool_name=tool_name,
                    arguments=tool_call_payload["args"],
                    result=tool_result,
                )
            )
            messages.append(
                ToolMessage(
                    content=json.dumps(tool_result, ensure_ascii=True),
                    name=tool_name,
                    tool_call_id=tool_call_payload["id"],
                )
            )

    raise RuntimeError(
        f"Tool calling loop exceeded {max_steps} steps for query: {query}"
    )
