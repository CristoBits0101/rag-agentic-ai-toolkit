# --- DEPENDENCIAS ---
import json
from collections.abc import Sequence

from langchain_core.messages import AIMessage
from langchain_core.messages import BaseMessage
from langchain_core.messages import HumanMessage
from langchain_core.messages import ToolMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langgraph.graph import END
from langgraph.graph import StateGraph

from config.react_agent_config import SYSTEM_PROMPT
from models.react_agent_entities import ReactAgentRunResult
from models.react_agent_entities import ReactToolStep
from models.react_agent_ollama_gateway import build_react_agent_ollama_chat_model
from models.react_agent_state import AgentState
from orchestration.react_tools_orchestration import build_react_tools
from orchestration.react_tools_orchestration import build_tools_by_name


def build_chat_prompt() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            MessagesPlaceholder(variable_name="scratch_pad"),
        ]
    )


def build_react_model(model=None, tools=None):
    llm = model or build_react_agent_ollama_chat_model()
    selected_tools = tools or build_react_tools()
    bound_model = llm.bind_tools(selected_tools) if hasattr(llm, "bind_tools") else llm
    return {
        "prompt": build_chat_prompt(),
        "bound_model": bound_model,
    }


def call_model(state: AgentState, model_react) -> dict[str, list[BaseMessage]]:
    prompt_value = model_react["prompt"].invoke({"scratch_pad": list(state["messages"])})
    prompt_messages = prompt_value.to_messages() if hasattr(prompt_value, "to_messages") else prompt_value
    response = model_react["bound_model"].invoke(prompt_messages)
    return {"messages": [response]}


def tool_node(state: AgentState, tools_by_name) -> dict[str, list[BaseMessage]]:
    last_message = state["messages"][-1]
    outputs: list[BaseMessage] = []

    for tool_call in getattr(last_message, "tool_calls", []) or []:
        tool = tools_by_name[tool_call["name"]]
        tool_result = tool.invoke(tool_call["args"])
        outputs.append(
            ToolMessage(
                content=json.dumps(tool_result),
                name=tool_call["name"],
                tool_call_id=tool_call["id"],
            )
        )

    return {"messages": outputs}


def should_continue(state: AgentState) -> str:
    last_message = state["messages"][-1]
    if not getattr(last_message, "tool_calls", None):
        return "end"
    return "continue"


def build_react_workflow(model=None, tools=None):
    selected_tools = tools or build_react_tools()
    tools_by_name = build_tools_by_name(selected_tools)
    model_react = build_react_model(model=model, tools=selected_tools)
    workflow = StateGraph(AgentState)

    def agent_node(state: AgentState):
        return call_model(state, model_react=model_react)

    def tools_node(state: AgentState):
        return tool_node(state, tools_by_name=tools_by_name)

    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tools_node)
    workflow.add_edge("tools", "agent")
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "continue": "tools",
            "end": END,
        },
    )
    workflow.set_entry_point("agent")
    return workflow.compile()


def extract_tool_steps(messages: Sequence[BaseMessage]) -> tuple[ReactToolStep, ...]:
    steps: list[ReactToolStep] = []
    for index, message in enumerate(messages):
        if isinstance(message, AIMessage) and getattr(message, "tool_calls", None):
            next_message = messages[index + 1] if index + 1 < len(messages) else None
            for tool_call in message.tool_calls:
                tool_result = None
                if isinstance(next_message, ToolMessage) and next_message.name == tool_call["name"]:
                    try:
                        tool_result = json.loads(next_message.content)
                    except Exception:
                        tool_result = next_message.content
                steps.append(
                    ReactToolStep(
                        tool_name=tool_call["name"],
                        arguments=tool_call.get("args", {}),
                        result=tool_result,
                    )
                )
    return tuple(steps)


def get_final_answer(messages: Sequence[BaseMessage]) -> str:
    for message in reversed(messages):
        if isinstance(message, AIMessage) and not getattr(message, "tool_calls", None):
            return str(message.content).strip()
    return ""


def get_workflow_mermaid(workflow) -> str:
    try:
        return workflow.get_graph().draw_mermaid()
    except Exception:
        return ""


def invoke_react_query(query: str, workflow=None, model=None, tools=None) -> ReactAgentRunResult:
    active_workflow = workflow or build_react_workflow(model=model, tools=tools)
    result = active_workflow.invoke({"messages": [HumanMessage(content=query)]})
    messages = tuple(result["messages"])
    return ReactAgentRunResult(
        query=query,
        final_answer=get_final_answer(messages),
        steps=extract_tool_steps(messages),
        messages=messages,
        mermaid_graph=get_workflow_mermaid(active_workflow),
    )