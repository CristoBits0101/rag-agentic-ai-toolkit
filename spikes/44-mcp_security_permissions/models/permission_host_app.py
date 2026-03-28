# --- DEPENDENCIAS ---
import re
import sys
from pathlib import Path

SPIKE_ROOT = Path(__file__).resolve().parents[1]
if str(SPIKE_ROOT) not in sys.path:
    sys.path.insert(0, str(SPIKE_ROOT))

from config.mcp_security_config import HOST_PORT
from config.mcp_security_config import RISK_LEVELS
from models.permission_client_base import MCPPermissionClient


class MCPPermissionHostApp(MCPPermissionClient):
    """Deterministic host app with permission awareness and approval flow."""

    def __init__(self, server_script: str, permissions_file: str | None = None, scripted_elicitation: list[dict] | None = None):
        super().__init__(server_script, permissions_file=permissions_file, scripted_elicitation=scripted_elicitation)
        self.conversation_history: list[dict[str, str]] = []
        self.pending_approval: dict[str, object] | None = None
        self.risk_levels = dict(RISK_LEVELS)
        self.mode = "local-deterministic-host"

    def assess_risk(self, tool_name: str, arguments: dict) -> dict[str, object]:
        risk_level = self.risk_levels.get(tool_name, "medium")
        permission = self.permissions.get(tool_name, "ask")
        description_map = {
            "low": "Safe operation with minimal impact",
            "medium": "Moderate impact because it modifies data",
            "high": "High impact because it is destructive",
            "critical": "Critical impact because it simulates system level control",
        }
        return {
            "tool": tool_name,
            "risk_level": risk_level,
            "permission": permission,
            "requires_approval": permission == "ask",
            "description": description_map.get(risk_level, "Moderate impact"),
            "arguments": arguments,
        }

    def _extract_text(self, result) -> str:
        if isinstance(result, list) and result:
            first = result[0]
            return first.text if hasattr(first, "text") else str(first)
        return str(result)

    async def _dispatch_tool(self, tool_name: str, arguments: dict, approved: bool = False) -> str:
        result = await self.call_tool_with_permission(tool_name, arguments, approved=approved)
        return self._extract_text(result)

    async def ask(self, query: str) -> str:
        lowered = query.lower().strip()

        if self.pending_approval and lowered in {"yes", "approve", "ok", "confirm", "y"}:
            pending = self.pending_approval
            self.pending_approval = None
            result = await self._dispatch_tool(pending["tool_name"], pending["arguments"], approved=True)
            answer = f"Operation approved and executed.\n\n{result}"
            self.conversation_history.extend([
                {"role": "user", "content": query},
                {"role": "assistant", "content": answer},
            ])
            return answer

        if self.pending_approval and lowered in {"no", "deny", "cancel", "n"}:
            self.pending_approval = None
            answer = "Operation cancelled by user."
            self.conversation_history.extend([
                {"role": "user", "content": query},
                {"role": "assistant", "content": answer},
            ])
            return answer

        self.conversation_history.append({"role": "user", "content": query})
        tool_name = ""
        arguments: dict[str, object] = {}

        write_match = re.search(
            r"(?:write|create) (?:a )?file (?:called )?([\w./-]+) with (?:the )?content[ :]+(.+)",
            query,
            re.IGNORECASE,
        )
        if not write_match:
            write_match = re.search(
                r"write a new file called ([\w./-]+) with the content[ :]+(.+)",
                query,
                re.IGNORECASE,
            )
        if write_match:
            tool_name = "write_file"
            arguments = {"filepath": write_match.group(1), "content": write_match.group(2).strip().strip('"')}
        elif lowered.startswith("read"):
            filepath = query.split()[-1]
            tool_name = "read_file"
            arguments = {"filepath": filepath}
        elif lowered.startswith("delete"):
            filepath = query.split()[-1]
            tool_name = "delete_file"
            arguments = {"filepath": filepath}
        elif lowered.startswith("execute") or lowered.startswith("run command"):
            command = query.split(":", 1)[1].strip() if ":" in query else query.split(" ", 1)[1]
            tool_name = "execute_command"
            arguments = {"command": command}
        elif "audit" in lowered:
            contents = await self.read_resource("file://audit/log")
            answer = contents[0].text if contents and hasattr(contents[0], "text") else str(contents)
            self.conversation_history.append({"role": "assistant", "content": answer})
            return answer
        elif "prompt" in lowered or "security review" in lowered:
            messages = await self.get_prompt("security_review", {"operation": "write_file", "risk_level": "MEDIUM"})
            answer = "\n".join(
                message.content.text if hasattr(message.content, "text") else str(message.content)
                for message in messages
            )
            self.conversation_history.append({"role": "assistant", "content": answer})
            return answer
        else:
            answer = "I can read files write files delete files simulate commands and show audit information."
            self.conversation_history.append({"role": "assistant", "content": answer})
            return answer

        assessment = self.assess_risk(tool_name, arguments)
        result = await self._dispatch_tool(tool_name, arguments)
        if "Permission required for tool:" in result:
            self.pending_approval = {"tool_name": tool_name, "arguments": arguments}
            answer = (
                f"Risk: {assessment['risk_level']} - {assessment['description']}\n\n"
                f"{result}\nType yes to approve or no to cancel."
            )
        else:
            answer = f"Risk: {assessment['risk_level']} - {assessment['description']}\n\n{result}"
        self.conversation_history.append({"role": "assistant", "content": answer})
        return answer

    def _permission_summary(self) -> str:
        lines = ["### Current Permission Policies", ""]
        for tool_name, policy in self.permissions.items():
            lines.append(f"- **{tool_name}**: {policy.upper()} (Risk: {self.risk_levels.get(tool_name, 'medium')})")
        return "\n".join(lines)

    def create_interface(self):
        import gradio as gr

        async def chat_wrapper(message, history):
            if not message.strip():
                return history
            response = await self.ask(message)
            return history + [{"role": "user", "content": message}, {"role": "assistant", "content": response}]

        async def clear_history():
            self.conversation_history = []
            self.pending_approval = None
            return []

        with gr.Blocks(title="MCP Permission Host") as interface:
            gr.Markdown(
                f"# MCP Permission AI Host\n\n**Mode:** {self.mode}\n\n"
                "All tool executions are subject to permission policies and audit logging."
            )
            chatbot = gr.Chatbot(label="Conversation", height=500, type="messages")
            with gr.Row():
                message = gr.Textbox(label="Your message", placeholder="Ask me to use MCP tools", scale=4)
                clear = gr.Button("Clear", scale=1)
            with gr.Accordion("Permission Status", open=False):
                gr.Markdown(self._permission_summary())
            message.submit(fn=chat_wrapper, inputs=[message, chatbot], outputs=chatbot).then(lambda: "", outputs=message)
            clear.click(fn=clear_history, outputs=chatbot)
        return interface


def main():
    if len(sys.argv) < 2:
        print("Usage: python permission_host_app.py <server_script>")
        sys.exit(1)
    app = MCPPermissionHostApp(sys.argv[1])
    interface = app.create_interface()
    interface.queue().launch(server_name="127.0.0.1", server_port=HOST_PORT)


if __name__ == "__main__":
    main()