# --- DEPENDENCIAS ---
import asyncio
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPIKE = ROOT / "spikes" / "42-custom_mcp_client"

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
    "spike_42_custom_mcp_client_main",
    SPIKE / "main.py",
)
module = importlib.util.module_from_spec(module_spec)
assert module_spec is not None and module_spec.loader is not None
module_spec.loader.exec_module(module)
sys.path[:] = original_sys_path
run_custom_client_demo = module.run_custom_client_demo


def test_custom_client_demo_covers_tools_resources_and_prompts():
    result = asyncio.run(run_custom_client_demo())

    assert "echo" in result["tool_names"]
    assert "write_file" in result["tool_names"]
    assert any(template == "file://resources/{filename}" for template in result["resource_templates"])
    assert "review_file" in result["prompt_names"]
    assert result["echo_text"] == "Echo: Hello MCP!"
    assert "Successfully wrote to test.txt" in result["write_text"]
    assert "Project Name: MCP Client Lab" in result["resource_text"]
    assert "Please review the file 'test.txt'" in result["prompt_text"]