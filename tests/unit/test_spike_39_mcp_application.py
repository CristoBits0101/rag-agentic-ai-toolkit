# --- DEPENDENCIAS ---
import asyncio
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPIKE = ROOT / "spikes" / "39-mcp_application"

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
    "spike_39_mcp_application_workflow",
    SPIKE / "orchestration" / "mcp_application_workflow.py",
)
workflow = importlib.util.module_from_spec(module_spec)
assert module_spec is not None and module_spec.loader is not None
module_spec.loader.exec_module(workflow)
sys.path[:] = original_sys_path
run_mcp_application_demo = workflow.run_mcp_application_demo


def test_mcp_application_demo_handles_docs_museum_and_memory():
    result = asyncio.run(run_mcp_application_demo())

    assert "Available tools" in result["intro"]
    assert "FastMCP" in result["docs_answer"]
    assert "Van Gogh" in result["museum_answer"] or "Vincent van Gogh" in result["museum_answer"]
    assert "remember" in result["memory_answer"].lower()