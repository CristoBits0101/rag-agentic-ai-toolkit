# --- DEPENDENCIAS ---
import json
from typing import Any

from langchain_core.messages import HumanMessage
from langchain_core.messages import SystemMessage
from langchain_core.messages import ToolMessage
from langchain_core.tools import BaseTool

from config.datawizard_config import DATAWIZARD_SYSTEM_PROMPT
from config.datawizard_config import MAX_DATAWIZARD_STEPS
from models.datawizard_entities import DataWizardRunResult
from models.datawizard_entities import DataWizardStep
from models.datawizard_ollama_gateway import build_datawizard_ollama_chat_model
from orchestration.datawizard_tools_orchestration import build_datawizard_tools


def normalize_tool_result(raw_result: Any) -> dict[str, Any]:
    if isinstance(raw_result, dict):
        return raw_result

    return {"result": raw_result}


def execute_datawizard_query(
    query: str,
    tools: list[BaseTool] | None = None,
    model=None,
    max_steps: int = MAX_DATAWIZARD_STEPS,
) -> DataWizardRunResult:
    selected_tools = tools or build_datawizard_tools()
    selected_model = model or build_datawizard_ollama_chat_model()
    bound_model = selected_model.bind_tools(selected_tools)
    tool_map = {tool.name: tool for tool in selected_tools}
    messages = [
        SystemMessage(content=DATAWIZARD_SYSTEM_PROMPT),
        HumanMessage(content=query),
    ]
    steps: list[DataWizardStep] = []

    for _ in range(max_steps):
        ai_message = bound_model.invoke(messages)
        messages.append(ai_message)

        if not ai_message.tool_calls:
            return DataWizardRunResult(
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
                DataWizardStep(
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
        f"DataWizard exceeded {max_steps} steps for query: {query}"
    )
