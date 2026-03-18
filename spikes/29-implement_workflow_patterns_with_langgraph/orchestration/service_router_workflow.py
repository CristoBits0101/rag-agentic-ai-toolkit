# --- DEPENDENCIAS ---
from langgraph.graph import StateGraph

from models.workflow_patterns_state import ServiceRouterState


def classify_service_request(user_input: str) -> str:
    lowered = user_input.lower()
    if any(token in lowered for token in ["ride", "airport", "pickup", "downtown"]):
        return "ride_hailing_call"
    if any(token in lowered for token in ["pizza", "restaurant", "delivery", "order"]):
        return "restaurant_order"
    if any(token in lowered for token in ["milk", "bread", "eggs", "grocer", "vegetables"]):
        return "groceries"
    return "default_handler"


def router_node(state: ServiceRouterState) -> ServiceRouterState:
    return {**state, "task_type": classify_service_request(state["user_input"])}


def router(state: ServiceRouterState) -> str:
    return state["task_type"]


def ride_hailing_node(state: ServiceRouterState, model) -> ServiceRouterState:
    prompt = (
        "You are a ride hailing assistant. Extract pickup location destination timing "
        "and special requirements from the request.\n\n"
        f"User Request: {state['user_input']}"
    )
    response = model.invoke(prompt)
    return {**state, "task_type": "ride_hailing_call", "output": str(getattr(response, 'content', response)).strip()}


def restaurant_order_node(state: ServiceRouterState, model) -> ServiceRouterState:
    prompt = (
        "You are a restaurant ordering assistant. Organize menu items quantities "
        "delivery preference and timing.\n\n"
        f"User Request: {state['user_input']}"
    )
    response = model.invoke(prompt)
    return {**state, "task_type": "restaurant_order", "output": str(getattr(response, 'content', response)).strip()}


def groceries_node(state: ServiceRouterState, model) -> ServiceRouterState:
    prompt = (
        "You are a grocery delivery assistant. Create a practical shopping request with items "
        "quantities store hints and delivery notes.\n\n"
        f"User Request: {state['user_input']}"
    )
    response = model.invoke(prompt)
    return {**state, "task_type": "groceries", "output": str(getattr(response, 'content', response)).strip()}


def default_handler_node(state: ServiceRouterState, model) -> ServiceRouterState:
    prompt = (
        "You are a helpful support assistant. Explain that the request did not match the available services "
        "and suggest ride hailing restaurant orders or groceries.\n\n"
        f"User Request: {state['user_input']}"
    )
    response = model.invoke(prompt)
    return {**state, "task_type": "default_handler", "output": str(getattr(response, 'content', response)).strip()}


def build_service_router_workflow(model):
    workflow = StateGraph(ServiceRouterState)
    workflow.add_node("router", router_node)
    workflow.add_node("ride_hailing_call", lambda state: ride_hailing_node(state, model))
    workflow.add_node("restaurant_order", lambda state: restaurant_order_node(state, model))
    workflow.add_node("groceries", lambda state: groceries_node(state, model))
    workflow.add_node("default_handler", lambda state: default_handler_node(state, model))
    workflow.set_entry_point("router")
    workflow.add_conditional_edges(
        "router",
        router,
        {
            "ride_hailing_call": "ride_hailing_call",
            "restaurant_order": "restaurant_order",
            "groceries": "groceries",
            "default_handler": "default_handler",
        },
    )
    workflow.set_finish_point("ride_hailing_call")
    workflow.set_finish_point("restaurant_order")
    workflow.set_finish_point("groceries")
    workflow.set_finish_point("default_handler")
    return workflow.compile()


def invoke_service_router(user_input: str, model) -> ServiceRouterState:
    app = build_service_router_workflow(model)
    return app.invoke({"user_input": user_input, "task_type": "", "output": ""})