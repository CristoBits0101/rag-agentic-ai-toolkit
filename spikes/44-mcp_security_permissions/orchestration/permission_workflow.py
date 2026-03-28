# --- DEPENDENCIAS ---
from pathlib import Path

from config.mcp_security_config import CLIENT_AUDIT_LOG
from config.mcp_security_config import CLIENT_PERMISSIONS_FILE
from config.mcp_security_config import DATA_DIR
from config.mcp_security_config import DEFAULT_PERMISSIONS
from config.mcp_security_config import SAMPLE_FILE_CONTENT
from config.mcp_security_config import SAMPLE_FILE_NAME
from config.mcp_security_config import SERVER_AUDIT_LOG
from models.permission_client_base import MCPPermissionClient
from models.permission_host_app import MCPPermissionHostApp
from models.permission_mcp_server import ensure_data_files


def _first_text(result) -> str:
    first = result[0] if isinstance(result, list) and result else result
    return first.text if hasattr(first, "text") else str(first)


def _reset_demo_state():
    ensure_data_files()
    (DATA_DIR / SAMPLE_FILE_NAME).write_text(SAMPLE_FILE_CONTENT, encoding="utf-8")
    for path in [SERVER_AUDIT_LOG, CLIENT_AUDIT_LOG, CLIENT_PERMISSIONS_FILE, DATA_DIR / "host_permissions.json"]:
        if Path(path).exists():
            Path(path).unlink()


async def run_permission_demo() -> dict[str, object]:
    _reset_demo_state()
    server_script = str((Path(__file__).resolve().parents[1] / "models" / "permission_mcp_server.py").resolve())
    base_client = MCPPermissionClient(server_script, permissions_file=str(CLIENT_PERMISSIONS_FILE))
    base_client.permissions = dict(DEFAULT_PERMISSIONS)
    base_client.save_permissions()
    host_app = MCPPermissionHostApp(
        server_script,
        permissions_file=str(DATA_DIR / "host_permissions.json"),
        scripted_elicitation=[
            {"approved": True, "reason": "Need to create documentation artifact."},
            {"approved": True, "reason": "Need to create host artifact."},
        ],
    )
    host_app.permissions = dict(DEFAULT_PERMISSIONS)
    host_app.save_permissions()

    try:
        read_result = await base_client.call_tool_with_permission("read_file", {"filepath": SAMPLE_FILE_NAME})
        write_request = await base_client.call_tool_with_permission(
            "write_file",
            {"filepath": "new_file.txt", "content": "Test content"},
        )
        base_client.scripted_elicitation.append({"approved": True, "reason": "Required for the demo."})
        write_result = await base_client.call_tool_with_permission(
            "write_file",
            {"filepath": "new_file.txt", "content": "Test content"},
            approved=True,
        )
        delete_result = await base_client.call_tool_with_permission("delete_file", {"filepath": SAMPLE_FILE_NAME})
        prompt_messages = await base_client.get_prompt(
            "security_review",
            {"operation": "write_file", "risk_level": "MEDIUM"},
        )
        prompt_text = "\n".join(
            message.content.text if hasattr(message.content, "text") else str(message.content)
            for message in prompt_messages
        )
        server_audit = await base_client.read_resource("file://audit/log")
        server_audit_text = server_audit[0].text if server_audit and hasattr(server_audit[0], "text") else str(server_audit)

        host_request_text = await host_app.ask('Write a new file called greeting.txt with the content "Hello, world!"')
        host_approval_text = await host_app.ask("yes")
        host_denial_text = await host_app.ask("Delete the file test.txt")
    finally:
        await host_app.cleanup()
        await base_client.cleanup()

    client_audit_text = Path(CLIENT_AUDIT_LOG).read_text(encoding="utf-8") if Path(CLIENT_AUDIT_LOG).exists() else ""

    return {
        "read_text": _first_text(read_result),
        "write_request_text": _first_text(write_request),
        "write_result_text": _first_text(write_result),
        "delete_text": _first_text(delete_result),
        "prompt_text": prompt_text,
        "server_audit_text": server_audit_text,
        "client_audit_text": client_audit_text,
        "elicitation_count": len(base_client.elicitation_requests),
        "host_request_text": host_request_text,
        "host_approval_text": host_approval_text,
        "host_denial_text": host_denial_text,
    }