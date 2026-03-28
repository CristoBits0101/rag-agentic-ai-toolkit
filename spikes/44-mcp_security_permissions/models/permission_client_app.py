# --- DEPENDENCIAS ---
import json
import sys
from pathlib import Path

SPIKE_ROOT = Path(__file__).resolve().parents[1]
if str(SPIKE_ROOT) not in sys.path:
    sys.path.insert(0, str(SPIKE_ROOT))

from config.mcp_security_config import GUI_PORT
from models.permission_client_base import MCPPermissionClient


class MCPPermissionClientApp(MCPPermissionClient):
    """GUI client for permissions resources prompts and audit logs."""

    def __init__(self, server_script: str, permissions_file: str | None = None):
        super().__init__(server_script, permissions_file=permissions_file)
        self.tools_cache: list[str] = []

    async def gui_list_tools(self):
        import gradio as gr

        tools = await self.list_tools()
        lines = ["Available tools:", ""]
        self.tools_cache = []
        for tool in tools:
            permission = self.permissions.get(tool.name, "ask")
            self.tools_cache.append(tool.name)
            lines.append(f"- {tool.name}")
            lines.append(f"  Permission: {permission.upper()}")
            if tool.description:
                lines.append(f"  Description: {tool.description}")
            lines.append("")
        choices = [f"{name} ({self.permissions.get(name, 'ask')})" for name in self.tools_cache]
        return "\n".join(lines), gr.update(choices=choices)

    async def gui_call_tool(self, tool_selection: str, arguments_json: str, approved: bool = False):
        if not tool_selection:
            return "Please select a tool first"
        tool_name = tool_selection.split(" (", 1)[0]
        try:
            arguments = json.loads(arguments_json) if arguments_json.strip() else {}
        except json.JSONDecodeError as exc:
            return f"Invalid JSON in arguments: {exc}"
        result = await self.call_tool_with_permission(tool_name, arguments, approved=approved)
        first = result[0] if isinstance(result, list) and result else result
        return first.text if hasattr(first, "text") else str(first)

    async def gui_list_resources(self):
        resources = await self.list_resources()
        lines = ["Available resources:", ""]
        for resource in resources:
            lines.append(f"- {resource.uri}")
            if resource.name:
                lines.append(f"  Name: {resource.name}")
            if resource.description:
                lines.append(f"  Description: {resource.description}")
            lines.append("")
        return "\n".join(lines)

    async def gui_read_resource(self, uri: str):
        if not uri.strip():
            return "Please enter a resource URI"
        contents = await self.read_resource(uri)
        first = contents[0] if isinstance(contents, list) and contents else contents
        return first.text if hasattr(first, "text") else str(first)

    async def gui_list_prompts(self):
        import gradio as gr

        prompts = await self.list_prompts()
        lines = ["Available prompts:", ""]
        choices = []
        for prompt in prompts:
            choices.append(prompt.name)
            lines.append(f"- {prompt.name}")
            if prompt.description:
                lines.append(f"  Description: {prompt.description}")
            if prompt.arguments:
                lines.append(f"  Arguments: {', '.join(argument.name for argument in prompt.arguments)}")
            lines.append("")
        return "\n".join(lines), gr.update(choices=choices)

    async def gui_get_prompt(self, prompt_name: str, arguments_json: str):
        if not prompt_name:
            return "Please select a prompt first"
        try:
            arguments = json.loads(arguments_json) if arguments_json.strip() else {}
        except json.JSONDecodeError as exc:
            return f"Invalid JSON in arguments: {exc}"
        messages = await self.get_prompt(prompt_name, arguments)
        lines = [f"Prompt: {prompt_name}", ""]
        for message in messages:
            content = message.content.text if hasattr(message.content, "text") else str(message.content)
            lines.append(f"[{message.role}]: {content}")
            lines.append("")
        return "\n".join(lines)

    async def gui_configure_permission(self, tool_name: str, policy: str):
        if not tool_name:
            return "Please enter a tool name"
        if policy not in {"allow", "deny", "ask"}:
            return "Policy must be: allow deny or ask"
        self.permissions[tool_name] = policy
        self.save_permissions()
        return f"Permission updated: {tool_name} = {policy}"

    async def gui_view_audit_log(self):
        if not self.audit_log_file.exists():
            return "No audit log entries yet."
        return self.audit_log_file.read_text(encoding="utf-8")

    def create_interface(self):
        import gradio as gr

        async def gui_approve_tool(tool_selection, arguments_json):
            return await self.gui_call_tool(tool_selection, arguments_json, approved=True)

        async def load_tools_for_dropdown():
            tools = await self.list_tools()
            return gr.Dropdown(choices=[tool.name for tool in tools])

        with gr.Blocks(title="MCP Permission Client") as interface:
            gr.Markdown("# MCP Permission Client\n\nManage permissions audit logs and secure tool calls.")
            with gr.Tabs():
                with gr.Tab("Tools"):
                    with gr.Row():
                        with gr.Column():
                            list_tools_btn = gr.Button("List Tools", variant="primary")
                            tools_output = gr.Textbox(label="Available Tools", lines=10)
                        with gr.Column():
                            tool_dropdown = gr.Dropdown(label="Select Tool", choices=[], interactive=True)
                            tool_args = gr.Textbox(label="Arguments", placeholder='{"filepath": "test.txt"}', lines=3)
                            with gr.Row():
                                call_tool_btn = gr.Button("Call Tool", variant="primary")
                                approve_tool_btn = gr.Button("Approve & Execute")
                            tool_result = gr.Textbox(label="Result", lines=10)
                    list_tools_btn.click(fn=self.gui_list_tools, outputs=[tools_output, tool_dropdown])
                    call_tool_btn.click(fn=self.gui_call_tool, inputs=[tool_dropdown, tool_args], outputs=tool_result)
                    approve_tool_btn.click(fn=gui_approve_tool, inputs=[tool_dropdown, tool_args], outputs=tool_result)

                with gr.Tab("Resources"):
                    with gr.Row():
                        with gr.Column():
                            list_resources_btn = gr.Button("List Resources", variant="primary")
                            resources_output = gr.Textbox(label="Resources", lines=10)
                        with gr.Column():
                            resource_uri = gr.Textbox(label="Resource URI", placeholder="file://audit/log")
                            read_resource_btn = gr.Button("Read Resource", variant="primary")
                            resource_output = gr.Textbox(label="Content", lines=10)
                    list_resources_btn.click(fn=self.gui_list_resources, outputs=resources_output)
                    read_resource_btn.click(fn=self.gui_read_resource, inputs=resource_uri, outputs=resource_output)

                with gr.Tab("Prompts"):
                    with gr.Row():
                        with gr.Column():
                            list_prompts_btn = gr.Button("List Prompts", variant="primary")
                            prompts_output = gr.Textbox(label="Prompts", lines=6)
                        with gr.Column():
                            prompt_dropdown = gr.Dropdown(label="Select Prompt", choices=[], interactive=True)
                            prompt_args = gr.Textbox(
                                label="Arguments",
                                placeholder='{"operation": "write_file", "risk_level": "MEDIUM"}',
                                lines=2,
                            )
                            get_prompt_btn = gr.Button("Get Prompt", variant="primary")
                            prompt_result = gr.Textbox(label="Prompt Result", lines=10)
                    list_prompts_btn.click(fn=self.gui_list_prompts, outputs=[prompts_output, prompt_dropdown])
                    get_prompt_btn.click(fn=self.gui_get_prompt, inputs=[prompt_dropdown, prompt_args], outputs=prompt_result)

                with gr.Tab("Permissions"):
                    with gr.Row():
                        with gr.Column():
                            load_tools_btn = gr.Button("Load Tools")
                            perm_tool_name = gr.Dropdown(label="Tool Name", choices=[], allow_custom_value=True)
                            perm_policy = gr.Radio(choices=["allow", "deny", "ask"], label="Policy", value="ask")
                            save_permission_btn = gr.Button("Save Permission", variant="primary")
                            perm_result = gr.Textbox(label="Permission Result", lines=3)
                        with gr.Column():
                            audit_btn = gr.Button("View Audit Log")
                            audit_output = gr.Textbox(label="Audit Log", lines=15)
                    load_tools_btn.click(fn=load_tools_for_dropdown, outputs=perm_tool_name)
                    save_permission_btn.click(
                        fn=self.gui_configure_permission,
                        inputs=[perm_tool_name, perm_policy],
                        outputs=perm_result,
                    )
                    audit_btn.click(fn=self.gui_view_audit_log, outputs=audit_output)
        return interface


def main():
    if len(sys.argv) < 2:
        print("Usage: python permission_client_app.py <server_script>")
        sys.exit(1)
    app = MCPPermissionClientApp(sys.argv[1])
    interface = app.create_interface()
    interface.queue().launch(server_name="127.0.0.1", server_port=GUI_PORT)


if __name__ == "__main__":
    main()