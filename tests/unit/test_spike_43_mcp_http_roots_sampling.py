# --- DEPENDENCIAS ---
import asyncio
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPIKE = ROOT / "spikes" / "43-mcp_http_roots_sampling"

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
    "spike_43_advanced_http_workflow",
    SPIKE / "orchestration" / "advanced_http_workflow.py",
)
workflow = importlib.util.module_from_spec(module_spec)
assert module_spec is not None and module_spec.loader is not None
module_spec.loader.exec_module(workflow)
sys.path[:] = original_sys_path
run_advanced_http_demo = workflow.run_advanced_http_demo


def test_advanced_http_demo_covers_roots_sampling_and_host_flow():
    result = asyncio.run(run_advanced_http_demo())

    assert "list_roots_boundary" in result["tool_names"]
    assert "analyze_code" in result["tool_names"]
    assert "Workspace" in result["declared_roots"]
    assert "Declared client roots" in result["roots_text"]
    assert "FILE: README.md" in result["list_text"]
    assert "Successfully wrote" in result["write_text"]
    assert "This is a test file in the workspace." in result["resource_text"]
    assert "Please review the code" in result["prompt_text"]
    assert "Sampling analysis for security" in result["sampling_text"]
    assert result["sampling_requests"]
    assert "I created hello.txt" in result["host_write_text"]
    assert "Declared client roots" in result["host_roots_text"]