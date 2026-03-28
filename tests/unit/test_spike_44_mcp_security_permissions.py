# --- DEPENDENCIAS ---
import asyncio
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPIKE = ROOT / "spikes" / "44-mcp_security_permissions"

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
    "spike_44_permission_workflow",
    SPIKE / "orchestration" / "permission_workflow.py",
)
workflow = importlib.util.module_from_spec(module_spec)
assert module_spec is not None and module_spec.loader is not None
module_spec.loader.exec_module(workflow)
sys.path[:] = original_sys_path
run_permission_demo = workflow.run_permission_demo


def test_permission_demo_covers_permissions_elicitation_and_audit_logging():
    result = asyncio.run(run_permission_demo())

    assert "Sample content for testing" in result["read_text"]
    assert "Permission required for tool: write_file" in result["write_request_text"]
    assert "Successfully wrote to new_file.txt" in result["write_result_text"]
    assert "Permission denied for tool: delete_file" in result["delete_text"]
    assert "Review this operation for security implications" in result["prompt_text"]
    assert "WRITE: new_file.txt" in result["server_audit_text"]
    assert "TOOL: write_file - Decision: ASK" in result["client_audit_text"]
    assert result["elicitation_count"] >= 1
    assert "Type yes to approve" in result["host_request_text"]
    assert "Operation approved and executed" in result["host_approval_text"]
    assert "Permission denied for tool: delete_file" in result["host_denial_text"]