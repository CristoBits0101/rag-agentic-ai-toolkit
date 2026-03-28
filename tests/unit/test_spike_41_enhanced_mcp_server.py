# --- DEPENDENCIAS ---
import asyncio
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPIKE = ROOT / "spikes" / "41-enhanced_mcp_server"

spikes_root = str((ROOT / "spikes").resolve())
current_spike = str(SPIKE.resolve())
original_sys_path = list(sys.path)
sys.path[:] = [
    current_spike,
    *[
        path
        for path in sys.path
        if current_spike != path and spikes_root not in path
    ],
]

for module_name in list(sys.modules):
    if module_name == "main" or module_name.startswith("main."):
        sys.modules.pop(module_name)
    if module_name == "models" or module_name.startswith("models."):
        sys.modules.pop(module_name)
    if module_name == "orchestration" or module_name.startswith("orchestration."):
        sys.modules.pop(module_name)
    if module_name == "config" or module_name.startswith("config."):
        sys.modules.pop(module_name)

module_spec = importlib.util.spec_from_file_location(
    "spike_41_enhanced_mcp_workflow",
    SPIKE / "orchestration" / "enhanced_mcp_workflow.py",
)
workflow = importlib.util.module_from_spec(module_spec)
assert module_spec is not None and module_spec.loader is not None
module_spec.loader.exec_module(workflow)
sys.path[:] = original_sys_path
run_enhanced_mcp_demo = workflow.run_enhanced_mcp_demo


def test_enhanced_mcp_demo_writes_reviews_and_documentation():
    result = asyncio.run(run_enhanced_mcp_demo())

    assert "def add" in result["file_content"]
    assert "Code review for sample_subject.py" in result["review_output"]
    assert "sample_subject_docs.md" in result["documentation_output"]
    assert "# Documentation for sample_subject.py" in result["generated_text"]
    assert any("Write complete" in entry for entry in result["progress_log"])