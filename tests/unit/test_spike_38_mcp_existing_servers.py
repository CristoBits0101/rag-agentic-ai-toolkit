# --- DEPENDENCIAS ---
import asyncio
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPIKE = ROOT / "spikes" / "38-mcp_existing_servers"

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
    "spike_38_mcp_existing_servers_workflow",
    SPIKE / "orchestration" / "mcp_existing_servers_workflow.py",
)
workflow = importlib.util.module_from_spec(module_spec)
assert module_spec is not None and module_spec.loader is not None
module_spec.loader.exec_module(workflow)
sys.path[:] = original_sys_path
build_stdio_transport = workflow.build_stdio_transport
describe_real_world_transport_targets = workflow.describe_real_world_transport_targets
list_tools_with_transport = workflow.list_tools_with_transport
local_http_server = workflow.local_http_server
build_http_transport = workflow.build_http_transport
resolve_and_query_fastmcp = workflow.resolve_and_query_fastmcp


def test_real_world_targets_document_real_context7_endpoints():
    targets = describe_real_world_transport_targets()

    assert "@upstash/context7-mcp" in targets["stdio_command"]
    assert targets["http_url"].startswith("https://")


def test_stdio_transport_lists_context7_tools():
    tools = asyncio.run(list_tools_with_transport(build_stdio_transport()))

    assert "resolve-library-id" in tools
    assert "query-docs" in tools


def test_http_transport_queries_fastmcp_docs():
    async def scenario():
        async with local_http_server() as url:
            payload = await resolve_and_query_fastmcp(build_http_transport(url))
            return payload

    payload = asyncio.run(scenario())

    assert "FastMCP" in payload["resolve_text"]
    assert "Register tools with @mcp.tool" in payload["docs_text"]