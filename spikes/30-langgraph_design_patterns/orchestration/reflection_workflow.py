# --- DEPENDENCIAS ---
from langgraph.graph import END
from langgraph.graph import START
from langgraph.graph import StateGraph

from models.design_patterns_state import ReflectionState


def determine_target_grade(state: ReflectionState):
    profile = state["investor_profile"].lower()
    if "risk tolerance: high" in profile:
        return {"target_grade": "aggressive"}
    if "risk tolerance: low" in profile:
        return {"target_grade": "conservative"}
    return {"target_grade": "moderate"}


def investment_plan_generator(state: ReflectionState, model):
    if state.get("feedback"):
        prompt = (
            "You are an adaptive investment advisor inspired by Ray Dalio. Improve the plan based on the investor profile and feedback. "
            f"Investor profile:\n{state['investor_profile']}\n\n"
            f"Previous grade: {state.get('grade', '')}\n"
            f"Feedback: {state.get('feedback', '')}"
        )
    else:
        prompt = (
            "You are a bold innovation driven investment advisor inspired by Cathie Wood. Write a concise investment plan.\n\n"
            f"Investor profile:\n{state['investor_profile']}"
        )
    response = model.invoke(prompt)
    return {"investment_plan": str(getattr(response, 'content', response)).strip()}


def evaluate_plan(state: ReflectionState):
    current_count = state.get("n", 0) + 1
    plan = state.get("investment_plan", "").lower()
    if any(token in plan for token in ["cryptocurrency", "leveraged", "speculative"]):
        grade = "high risk"
        feedback = "The plan leans on speculative assets and increases downside risk."
    elif any(token in plan for token in ["growth", "technology", "innovation", "equity"]):
        grade = "aggressive"
        feedback = "The plan emphasizes growth assets and accepts elevated volatility."
    elif any(token in plan for token in ["bonds", "treasury", "dividend", "cash"]):
        grade = "conservative"
        feedback = "The plan emphasizes capital preservation and stable assets."
    else:
        grade = "moderate"
        feedback = "The plan is balanced but could align more clearly with the target profile."
    return {"grade": grade, "feedback": feedback, "n": current_count}


def route_investment(state: ReflectionState, iteration_limit: int = 3):
    if state.get("grade") == state.get("target_grade"):
        return "Accepted"
    if state.get("n", 0) > iteration_limit:
        return "Accepted"
    return "Rejected + Feedback"


def build_reflection_workflow(model):
    builder = StateGraph(ReflectionState)
    builder.add_node("determine_target_grade", determine_target_grade)
    builder.add_node("investment_plan_generator", lambda state: investment_plan_generator(state, model))
    builder.add_node("evaluate_plan", evaluate_plan)
    builder.add_edge(START, "determine_target_grade")
    builder.add_edge("determine_target_grade", "investment_plan_generator")
    builder.add_edge("investment_plan_generator", "evaluate_plan")
    builder.add_conditional_edges(
        "evaluate_plan",
        lambda state: route_investment(state),
        {"Accepted": END, "Rejected + Feedback": "investment_plan_generator"},
    )
    return builder.compile()


def invoke_reflection_workflow(investor_profile: str, model) -> ReflectionState:
    app = build_reflection_workflow(model)
    return app.invoke(
        {
            "investment_plan": "",
            "investor_profile": investor_profile,
            "target_grade": "moderate",
            "feedback": "",
            "grade": "moderate",
            "n": 0,
        }
    )