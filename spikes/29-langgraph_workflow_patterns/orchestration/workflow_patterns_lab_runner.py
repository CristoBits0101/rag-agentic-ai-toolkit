# --- DEPENDENCIAS ---
from config.workflow_patterns_config import PARALLEL_EXAMPLE_TEXT
from config.workflow_patterns_config import PROMPT_CHAIN_JOB_DESCRIPTION
from config.workflow_patterns_config import ROUTER_EXAMPLES
from config.workflow_patterns_config import SERVICE_ROUTER_EXAMPLES
from models.workflow_patterns_ollama_gateway import build_workflow_patterns_model
from orchestration.parallel_workflow import build_parallel_translation_workflow
from orchestration.parallel_workflow import invoke_parallel_translation
from orchestration.prompt_chaining_workflow import build_prompt_chaining_workflow
from orchestration.prompt_chaining_workflow import invoke_job_application_workflow
from orchestration.routing_workflow import build_task_router_workflow
from orchestration.routing_workflow import invoke_task_router
from orchestration.service_router_workflow import build_service_router_workflow
from orchestration.service_router_workflow import invoke_service_router


def print_divider(title: str) -> None:
    print(f"\n=== {title} ===")


def run_workflow_patterns_demo() -> None:
    model = build_workflow_patterns_model()

    print_divider("Prompt Chaining")
    chain_result = invoke_job_application_workflow(PROMPT_CHAIN_JOB_DESCRIPTION, model)
    print(chain_result["resume_summary"])
    print()
    print(chain_result["cover_letter"])
    print(build_prompt_chaining_workflow(model).get_graph().draw_mermaid())

    print_divider("Routing")
    router_app = build_task_router_workflow(model)
    for example in ROUTER_EXAMPLES:
        result = invoke_task_router(example, model)
        print(f"Input: {example}")
        print(f"Task Type: {result['task_type']}")
        print(f"Output: {result['output']}")
        print("-")
    print(router_app.get_graph().draw_mermaid())

    print_divider("Parallelization")
    parallel_result = invoke_parallel_translation(PARALLEL_EXAMPLE_TEXT, model)
    print(parallel_result["combined_output"])
    print(build_parallel_translation_workflow(model).get_graph().draw_mermaid())

    print_divider("Multi Agent Routing Exercise")
    service_app = build_service_router_workflow(model)
    for example in SERVICE_ROUTER_EXAMPLES:
        result = invoke_service_router(example, model)
        print(f"Input: {example}")
        print(f"Task Type: {result['task_type']}")
        print(f"Output: {result['output']}")
        print("-")
    print(service_app.get_graph().draw_mermaid())