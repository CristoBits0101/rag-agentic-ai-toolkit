# --- DEPENDENCIAS ---
from langchain_core.tools import BaseTool

from models.interactive_agents_ollama_gateway import build_interactive_agents_ollama_chat_model
from orchestration.interactive_agents_manual_tool_calling_orchestration import (
    execute_manual_tool_calling_query,
)
from orchestration.interactive_agents_tools_orchestration import build_interactive_math_tools
from orchestration.interactive_agents_tools_orchestration import build_tip_tools


class ToolCallingAgent:
    def __init__(self, model=None, tools: list[BaseTool] | None = None):
        self._model = model or build_interactive_agents_ollama_chat_model()
        self._tools = tools or build_interactive_math_tools()

    def run(self, query: str) -> str:
        return execute_manual_tool_calling_query(
            query=query,
            tools=self._tools,
            model=self._model,
        ).final_answer


class TipAgent:
    def __init__(self, model=None, tools: list[BaseTool] | None = None):
        self._model = model or build_interactive_agents_ollama_chat_model()
        self._tools = tools or build_tip_tools()

    def run(self, query: str) -> str:
        return execute_manual_tool_calling_query(
            query=query,
            tools=self._tools,
            model=self._model,
        ).final_answer
