# --- DEPENDENCIAS ---
from datetime import datetime
from pathlib import Path
import json
import sys

SPIKE_ROOT = Path(__file__).resolve().parents[1]
if str(SPIKE_ROOT) not in sys.path:
    sys.path.insert(0, str(SPIKE_ROOT))

from fastmcp import Context
from fastmcp import FastMCP
from pydantic import BaseModel

from config.mcp_security_config import DATA_DIR
from config.mcp_security_config import DEFAULT_PERMISSIONS
from config.mcp_security_config import SAMPLE_FILE_CONTENT
from config.mcp_security_config import SAMPLE_FILE_NAME
from config.mcp_security_config import SERVER_AUDIT_LOG

mcp = FastMCP("Permission-Aware MCP Server")


class WriteApprovalSchema(BaseModel):
    approved: bool
    reason: str


class DeleteApprovalSchema(BaseModel):
    approved: bool
    reason: str
    acknowledge_irreversible: bool


class CommandApprovalSchema(BaseModel):
    approved: bool
    purpose: str
    acknowledge_risk: bool


def ensure_data_files() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    sample_path = DATA_DIR / SAMPLE_FILE_NAME
    if not sample_path.exists():
        sample_path.write_text(SAMPLE_FILE_CONTENT, encoding="utf-8")


def resolve_data_path(filepath: str) -> Path:
    candidate = (DATA_DIR / filepath).resolve()
    candidate.relative_to(DATA_DIR.resolve())
    return candidate


def append_server_audit(action: str, details: str) -> None:
    ensure_data_files()
    with open(SERVER_AUDIT_LOG, "a", encoding="utf-8") as handle:
        handle.write(f"[{datetime.now().isoformat()}] {action}: {details}\n")


@mcp.tool()
def read_file(filepath: str) -> str:
    ensure_data_files()
    try:
        path = resolve_data_path(filepath)
    except ValueError:
        return "Error: Access denied - path outside data directory"
    if not path.exists() or not path.is_file():
        return f"Error: File {filepath} not found"
    return path.read_text(encoding="utf-8")


@mcp.tool()
async def write_file(filepath: str, content: str, ctx: Context) -> str:
    ensure_data_files()
    approval = await ctx.elicit(
        message=f"Approve writing to {filepath}",
        response_type=WriteApprovalSchema,
    )
    if approval.action != "accept" or not approval.data.approved:
        append_server_audit("WRITE_DECLINED", filepath)
        return f"Write declined for {filepath}"
    try:
        path = resolve_data_path(filepath)
    except ValueError:
        return "Error: Access denied - path outside data directory"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    append_server_audit("WRITE", f"{filepath} | reason={approval.data.reason}")
    return f"Successfully wrote to {filepath}"


@mcp.tool()
async def delete_file(filepath: str, ctx: Context) -> str:
    ensure_data_files()
    approval = await ctx.elicit(
        message=f"Approve deleting {filepath}",
        response_type=DeleteApprovalSchema,
    )
    if approval.action != "accept" or not approval.data.approved or not approval.data.acknowledge_irreversible:
        append_server_audit("DELETE_DECLINED", filepath)
        return f"Delete declined for {filepath}"
    try:
        path = resolve_data_path(filepath)
    except ValueError:
        return "Error: Access denied - path outside data directory"
    if not path.exists() or not path.is_file():
        return f"Error: File {filepath} not found"
    path.unlink()
    append_server_audit("DELETE", f"{filepath} | reason={approval.data.reason}")
    return f"Successfully deleted {filepath}"


@mcp.tool()
async def execute_command(command: str, ctx: Context) -> str:
    ensure_data_files()
    approval = await ctx.elicit(
        message=f"Approve simulated command execution: {command}",
        response_type=CommandApprovalSchema,
    )
    if approval.action != "accept" or not approval.data.approved or not approval.data.acknowledge_risk:
        append_server_audit("EXECUTE_DECLINED", command)
        return f"Execution declined for command: {command}"
    append_server_audit("EXECUTE", f"{command} | purpose={approval.data.purpose}")
    return f"Simulated execution of command: {command}\n(Actual execution disabled for security)"


@mcp.resource("file://audit/log")
def get_audit_log() -> str:
    ensure_data_files()
    if not SERVER_AUDIT_LOG.exists():
        return "No audit log entries yet."
    return SERVER_AUDIT_LOG.read_text(encoding="utf-8")


@mcp.resource("file://config/permissions")
def get_permissions_config() -> str:
    ensure_data_files()
    return json.dumps(DEFAULT_PERMISSIONS, indent=2)


@mcp.prompt()
def security_review(operation: str, risk_level: str) -> str:
    return (
        "Review this operation for security implications.\n\n"
        f"Operation: {operation}\n"
        f"Risk Level: {risk_level}\n\n"
        "Analyze affected systems safeguards approval requirements and audit needs."
    )


if __name__ == "__main__":
    ensure_data_files()
    mcp.run(transport="stdio")