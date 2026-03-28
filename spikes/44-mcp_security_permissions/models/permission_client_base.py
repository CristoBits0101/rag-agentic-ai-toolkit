# --- DEPENDENCIAS ---
from contextlib import AsyncExitStack
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace
import json
import sys

from mcp import ClientSession
from mcp import StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.types import ElicitResult

from config.mcp_security_config import CLIENT_AUDIT_LOG
from config.mcp_security_config import CLIENT_PERMISSIONS_FILE
from config.mcp_security_config import DEFAULT_PERMISSIONS


class MCPPermissionClient:
    """Base MCP client with permission checks audit logging and elicitation."""

    def __init__(self, server_script: str, permissions_file: str | None = None, scripted_elicitation: list[dict] | None = None):
        self.server_script = str(Path(server_script).resolve())
        self.permissions_file = Path(permissions_file or CLIENT_PERMISSIONS_FILE).resolve()
        self.permissions_file.parent.mkdir(parents=True, exist_ok=True)
        self.audit_log_file = Path(CLIENT_AUDIT_LOG).resolve()
        self.session = None
        self.exit_stack = AsyncExitStack()
        self._connected = False
        self.permissions = self.load_permissions()
        self.scripted_elicitation = list(scripted_elicitation or [])
        self.elicitation_requests: list[dict[str, object]] = []

    async def _handle_elicitation(self, _context, params) -> ElicitResult:
        schema = params.requestedSchema
        provided = self.scripted_elicitation.pop(0) if self.scripted_elicitation else {}
        action = provided.pop("__action__", "accept") if isinstance(provided, dict) else "accept"
        self.elicitation_requests.append({"message": params.message, "schema": schema, "action": action})
        if action != "accept":
            return ElicitResult(action=action)
        content: dict[str, object] = {}
        for field_name, field_schema in schema.get("properties", {}).items():
            if isinstance(provided, dict) and field_name in provided:
                content[field_name] = provided[field_name]
                continue
            field_type = field_schema.get("type", "string")
            if field_name == "approved":
                content[field_name] = True
            elif field_name in {"acknowledge_irreversible", "acknowledge_risk"}:
                content[field_name] = True
            elif field_type == "boolean":
                content[field_name] = True
            elif field_type == "integer":
                content[field_name] = 1
            elif field_type == "number":
                content[field_name] = 1.0
            else:
                content[field_name] = "Auto approved by demo client."
        return ElicitResult(action="accept", content=content)

    async def connect(self):
        if self._connected:
            return
        server_params = StdioServerParameters(command=sys.executable, args=[self.server_script], env=None)
        read, write = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(read, write, elicitation_callback=self._handle_elicitation)
        )
        await self.session.initialize()
        self._connected = True

    def load_permissions(self) -> dict:
        if self.permissions_file.exists():
            return json.loads(self.permissions_file.read_text(encoding="utf-8"))
        return dict(DEFAULT_PERMISSIONS)

    def save_permissions(self):
        self.permissions_file.write_text(json.dumps(self.permissions, indent=2), encoding="utf-8")

    def check_permission(self, tool_name: str, arguments: dict) -> str:
        arg_key = f"{tool_name}:{json.dumps(arguments, sort_keys=True)}"
        if arg_key in self.permissions:
            return self.permissions[arg_key]
        return self.permissions.get(tool_name, "ask")

    def log_audit(self, operation: str, decision: str, reason: str = ""):
        timestamp = datetime.now().isoformat()
        line = f"[{timestamp}] {operation} - Decision: {decision}"
        if reason:
            line += f" - Reason: {reason}"
        with open(self.audit_log_file, "a", encoding="utf-8") as handle:
            handle.write(line + "\n")

    async def list_tools(self):
        await self.connect()
        result = await self.session.list_tools()
        return result.tools

    async def call_tool_with_permission(self, tool_name: str, arguments: dict | None = None, approved: bool = False):
        await self.connect()
        resolved_arguments = arguments or {}
        permission = self.check_permission(tool_name, resolved_arguments)
        if permission == "deny":
            self.log_audit(f"TOOL: {tool_name}", "DENIED", "Policy: deny")
            return [SimpleNamespace(text=f"Permission denied for tool: {tool_name}")]
        if permission == "ask" and not approved:
            self.log_audit(f"TOOL: {tool_name}", "ASK", "Awaiting approval")
            message = (
                f"Permission required for tool: {tool_name}\n"
                f"Arguments: {json.dumps(resolved_arguments, indent=2, sort_keys=True)}\n\n"
                "This tool requires approval before execution.\n"
                "Please approve this operation in the GUI to proceed."
            )
            return [SimpleNamespace(text=message)]
        self.log_audit(f"TOOL: {tool_name}", "ALLOWED", f"Policy: {permission}")
        result = await self.session.call_tool(tool_name, arguments=resolved_arguments)
        return result.content

    async def list_resources(self):
        await self.connect()
        result = await self.session.list_resources()
        return result.resources

    async def read_resource(self, uri: str):
        await self.connect()
        result = await self.session.read_resource(uri=uri)
        return result.contents

    async def list_prompts(self):
        await self.connect()
        result = await self.session.list_prompts()
        return result.prompts

    async def get_prompt(self, prompt_name: str, arguments: dict | None = None):
        await self.connect()
        result = await self.session.get_prompt(name=prompt_name, arguments=arguments or {})
        return result.messages

    async def cleanup(self):
        await self.exit_stack.aclose()