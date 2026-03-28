# --- DEPENDENCIAS ---
from langgraph.graph import StateGraph

from models.workflow_patterns_state import RouterState


def classify_task(user_input: str) -> str:
    lowered = user_input.lower()
    if any(token in lowered for token in ["translate", "french", "spanish", "japanese"]):
        return "translate"
    return "summarize"


def router_node(state: RouterState) -> RouterState:
    return {**state, "task_type": classify_task(state["user_input"])}


def router(state: RouterState) -> str:
    return state["task_type"]


def summarize_node(state: RouterState, model) -> RouterState:
    prompt = f"Please summarize the following passage in two sentences.\n\n{state['user_input']}"
    response = model.invoke(prompt)
    content = getattr(response, "content", response)
    return {**state, "task_type": "summarize", "output": str(content).strip()}


def translate_node(state: RouterState, model) -> RouterState:
    prompt = f"Translate the following text to French.\n\n{state['user_input']}"
    response = model.invoke(prompt)
    content = getattr(response, "content", response)
    return {**state, "task_type": "translate", "output": str(content).strip()}


def build_task_router_workflow(model):
    workflow = StateGraph(RouterState)
    workflow.add_node("router", router_node)
    workflow.add_node("summarize", lambda state: summarize_node(state, model))
    workflow.add_node("translate", lambda state: translate_node(state, model))
    workflow.set_entry_point("router")
    workflow.add_conditional_edges("router", router, {"summarize": "summarize", "translate": "translate"})
    workflow.set_finish_point("summarize")
    workflow.set_finish_point("translate")
    return workflow.compile()


def invoke_task_router(user_input: str, model) -> RouterState:
    app = build_task_router_workflow(model)
    return app.invoke({"user_input": user_input, "task_type": "", "output": ""})