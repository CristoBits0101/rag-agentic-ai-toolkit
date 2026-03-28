# --- DEPENDENCIAS ---
from langgraph.constants import Send
from langgraph.graph import END
from langgraph.graph import START
from langgraph.graph import StateGraph

from config.design_patterns_config import MEAL_CATALOG
from models.design_patterns_entities import Dish
from models.design_patterns_state import OrchestrationState
from models.design_patterns_state import WorkerState


def parse_meals(meals: str) -> list[str]:
    normalized = meals.lower()
    matched_meals = []
    remaining = normalized

    for known_meal in sorted(MEAL_CATALOG, key=len, reverse=True):
        if known_meal in remaining:
            matched_meals.append(known_meal)
            remaining = remaining.replace(known_meal, " ")

    trailing_meals = [item.strip() for item in remaining.replace(" and ", ",").split(",") if item.strip()]
    return matched_meals + trailing_meals


def orchestrator(state: OrchestrationState):
    sections = []
    for meal in parse_meals(state["meals"]):
        payload = MEAL_CATALOG.get(meal, {"location": "Global", "ingredients": [meal, "salt", "pepper"]})
        sections.append(Dish(name=meal.title(), ingredients=payload["ingredients"], location=payload["location"]))
    return {"sections": sections}


def assign_workers(state: OrchestrationState):
    return [Send("chef_worker", {"section": section}) for section in state.get("sections", [])]


def chef_worker(state: WorkerState, model):
    section = state["section"]
    prompt = (
        f"You are a world class chef from {section.location}. Introduce yourself briefly and explain how to prepare {section.name}. "
        f"Use these ingredients: {', '.join(section.ingredients)}. Include steps and cooking process."
    )
    response = model.invoke(prompt)
    return {"completed_menu": [str(getattr(response, 'content', response)).strip()]}


def synthesizer(state: OrchestrationState):
    completed_sections = state.get("completed_menu", [])
    return {"final_meal_guide": "\n\n---\n\n".join(completed_sections)}


def build_orchestrator_worker_workflow(model):
    builder = StateGraph(OrchestrationState)
    builder.add_node("orchestrator", orchestrator)
    builder.add_node("chef_worker", lambda state: chef_worker(state, model))
    builder.add_node("synthesizer", synthesizer)
    builder.add_edge(START, "orchestrator")
    builder.add_conditional_edges("orchestrator", assign_workers, ["chef_worker"])
    builder.add_edge("chef_worker", "synthesizer")
    builder.add_edge("synthesizer", END)
    return builder.compile()


def invoke_orchestrator_worker(meals: str, model) -> OrchestrationState:
    app = build_orchestrator_worker_workflow(model)
    return app.invoke({"meals": meals, "sections": [], "completed_menu": [], "final_meal_guide": ""})