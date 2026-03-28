# --- DEPENDENCIAS ---
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPIKE = ROOT / "spikes" / "29-langgraph_workflow_patterns"

if str(SPIKE) not in sys.path:
    sys.path.insert(0, str(SPIKE))

for module_name in list(sys.modules):
    if module_name == "models" or module_name.startswith("models."):
        sys.modules.pop(module_name)
    if module_name == "orchestration" or module_name.startswith("orchestration."):
        sys.modules.pop(module_name)
    if module_name == "config" or module_name.startswith("config."):
        sys.modules.pop(module_name)

from orchestration.parallel_workflow import invoke_parallel_translation
from orchestration.prompt_chaining_workflow import invoke_job_application_workflow
from orchestration.routing_workflow import invoke_task_router
from orchestration.service_router_workflow import invoke_service_router


class FakeResponse:
    def __init__(self, content: str):
        self.content = content


class FakeModel:
    def invoke(self, prompt: str):
        lowered = prompt.lower()
        if "resume assistant" in lowered:
            return FakeResponse("Results driven data scientist with NLP machine learning and production experience.")
        if "cover letter" in lowered:
            return FakeResponse("Dear Hiring Team. I am excited to apply because my background matches the role.")
        if "translate the following text to french" in lowered:
            return FakeResponse("Bonjour. J'aime programmer.")
        if "translate the following text to spanish" in lowered:
            return FakeResponse("Buenos dias. Espero que tengas un gran dia.")
        if "translate the following text to japanese" in lowered:
            return FakeResponse("ãŠã¯ã‚ˆã†ã”ã–ã„ã¾ã™ã€‚ç´ æ™´ã‚‰ã—ã„ä¸€æ—¥ã«ãªã‚Šã¾ã™ã‚ˆã†ã«ã€‚")
        if "summarize" in lowered:
            return FakeResponse("This is a concise summary.")
        if "ride hailing assistant" in lowered:
            return FakeResponse("Pickup downtown. Dropoff airport. Time 3pm.")
        if "restaurant ordering assistant" in lowered:
            return FakeResponse("Order two large pepperoni pizzas for delivery tonight.")
        if "grocery delivery assistant" in lowered:
            return FakeResponse("Milk bread eggs and vegetables for weekly shopping.")
        return FakeResponse("Please choose one of the supported services.")


def test_prompt_chaining_workflow_generates_resume_and_cover_letter():
    result = invoke_job_application_workflow("Need a data scientist with NLP and Python.", FakeModel())
    assert "data scientist" in result["resume_summary"].lower()
    assert "dear hiring team" in result["cover_letter"].lower()


def test_routing_workflow_routes_translation_requests():
    result = invoke_task_router("Translate this sentence to French.", FakeModel())
    assert result["task_type"] == "translate"
    assert "bonjour" in result["output"].lower()


def test_parallel_workflow_combines_three_translations():
    result = invoke_parallel_translation("Good morning", FakeModel())
    assert "French:" in result["combined_output"]
    assert "Spanish:" in result["combined_output"]
    assert "Japanese:" in result["combined_output"]


def test_service_router_workflow_handles_groceries():
    result = invoke_service_router("I need milk bread eggs and vegetables for the week.", FakeModel())
    assert result["task_type"] == "groceries"
    assert "milk" in result["output"].lower()