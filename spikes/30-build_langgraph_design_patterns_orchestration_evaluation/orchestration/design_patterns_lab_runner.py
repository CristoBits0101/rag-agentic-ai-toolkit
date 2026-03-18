# --- DEPENDENCIAS ---
from config.design_patterns_config import INVESTOR_PROFILE
from config.design_patterns_config import MEAL_REQUEST
from models.design_patterns_ollama_gateway import build_design_patterns_model
from orchestration.orchestrator_worker_workflow import build_orchestrator_worker_workflow
from orchestration.orchestrator_worker_workflow import invoke_orchestrator_worker
from orchestration.reflection_workflow import build_reflection_workflow
from orchestration.reflection_workflow import invoke_reflection_workflow


def print_divider(title: str) -> None:
    print(f"\n=== {title} ===")


def pretty_print_final_state(state: dict) -> None:
    print("Final Investment Plan Summary")
    print("=" * 32)
    print(f"Investor Profile:\n{state['investor_profile']}")
    print(f"Target Risk Grade: {state['target_grade']}")
    print(f"Final Assigned Grade: {state['grade']}")
    print(f"Iterations Taken: {state['n']}")
    print(f"Feedback: {state['feedback']}")
    print(f"Investment Plan: {state['investment_plan']}")


def run_design_patterns_demo() -> None:
    model = build_design_patterns_model()

    print_divider("Orchestrator Worker Pattern")
    orchestration_state = invoke_orchestrator_worker(MEAL_REQUEST, model)
    print(orchestration_state["final_meal_guide"])
    print(build_orchestrator_worker_workflow(model).get_graph().draw_mermaid())

    print_divider("Reflection Pattern")
    reflection_state = invoke_reflection_workflow(INVESTOR_PROFILE, model)
    pretty_print_final_state(reflection_state)
    print(build_reflection_workflow(model).get_graph().draw_mermaid())