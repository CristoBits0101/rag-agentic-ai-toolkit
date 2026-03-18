# --- DEPENDENCIAS ---
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPIKE = ROOT / "spikes" / "31-crewai_101_building_multi_agent_ai_systems"

if str(SPIKE) not in sys.path:
    sys.path.insert(0, str(SPIKE))

for module_name in list(sys.modules):
    if module_name == "models" or module_name.startswith("models."):
        sys.modules.pop(module_name)
    if module_name == "orchestration" or module_name.startswith("orchestration."):
        sys.modules.pop(module_name)
    if module_name == "config" or module_name.startswith("config."):
        sys.modules.pop(module_name)

MODULE_PATH = SPIKE / "orchestration" / "content_creation_workflow.py"
MODULE_SPEC = importlib.util.spec_from_file_location("content_creation_workflow", MODULE_PATH)
CONTENT_WORKFLOW = importlib.util.module_from_spec(MODULE_SPEC)
assert MODULE_SPEC is not None
assert MODULE_SPEC.loader is not None
MODULE_SPEC.loader.exec_module(CONTENT_WORKFLOW)

build_content_creation_crew = CONTENT_WORKFLOW.build_content_creation_crew
run_content_pipeline = CONTENT_WORKFLOW.run_content_pipeline


class FakeResponse:
    def __init__(self, content: str):
        self.content = content


class FakeModel:
    def invoke(self, prompt: str):
        lowered = prompt.lower()
        if "three short social posts" in lowered:
            return FakeResponse("1. Local AI agents are getting more reliable.\n2. Structured workflows reduce failure rates.\n3. Open models widen deployment options.")
        if "four paragraph blog post" in lowered:
            return FakeResponse("Generative AI moved toward smaller multimodal systems. Teams are using structured agents. Open models improved deployability. The main trend is reliability.")
        return FakeResponse("Detailed report covering multimodal models structured agent workflows and open weight reasoning systems.")


def test_content_pipeline_generates_research_blog_and_social_outputs():
    summary = run_content_pipeline(topic="Latest Generative AI breakthroughs", model=FakeModel())
    assert "report" in summary.research_report.lower() or "multimodal" in summary.research_report.lower()
    assert "generative ai" in summary.blog_post.lower() or "structured agents" in summary.blog_post.lower()
    assert "1." in summary.social_posts


def test_content_creation_crew_exposes_three_task_outputs():
    crew, _, _, _ = build_content_creation_crew(model=FakeModel())
    result = crew.kickoff(inputs={"topic": "Latest Generative AI breakthroughs"})
    assert len(result.tasks_output) == 3
    assert result.token_usage.total_tokens > 0