# --- DEPENDENCIAS ---
import asyncio
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPIKE = ROOT / "spikes" / "40-mcp_hello_world"

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
    "spike_40_hello_mcp_workflow",
    SPIKE / "orchestration" / "hello_mcp_workflow.py",
)
workflow = importlib.util.module_from_spec(module_spec)
assert module_spec is not None and module_spec.loader is not None
module_spec.loader.exec_module(workflow)
sys.path[:] = original_sys_path
run_hello_world_mcp_demo = workflow.run_hello_world_mcp_demo


def test_hello_world_mcp_demo_covers_all_transports_and_prompting():
    result = asyncio.run(run_hello_world_mcp_demo())

    assert "add" in result["tools"]
    assert result["in_memory_add"] == "9"
    assert result["http_add"] == "9"
    assert result["stdio_add"] == "9"
    assert "Document contents of README.txt" in result["template_resource"]
    assert "Hello World MCP example readme" in result["disk_resource"]
    assert "Please review this code" in result["review_prompt"]
    assert any(tool_name == "add" for tool_name in result["multi_server"]["tool_names"])
    assert any(value == 15 for value in result["multi_server"]["add_results"])