# --- DEPENDENCIAS ---
import json
import sys
from pathlib import Path

SPIKE_ROOT = Path(__file__).resolve().parents[1]
if str(SPIKE_ROOT) not in sys.path:
    sys.path.insert(0, str(SPIKE_ROOT))

from config.advanced_mcp_http_config import GUI_PORT
from models.advanced_http_client_base import MCPHTTPClient


class MCPHTTPClientApp(MCPHTTPClient):
    """GUI client for manual interaction with the HTTP MCP server."""

    async def gui_list_tools(self):
        import gradio as gr

        tools = await self.list_tools()
        output = "\n".join(f"- {tool.name}: {tool.description}" for tool in tools)
        choices = [tool.name for tool in tools]
        return output, gr.update(choices=choices)

    async def gui_call_tool(self, tool_name: str, arguments_json: str):
        if not tool_name:
            return "Error: Please select a tool first"
        try:
            arguments = json.loads(arguments_json) if arguments_json else {}
        except json.JSONDecodeError:
            return "Error: Invalid JSON format"
        result = await self.call_tool(tool_name, arguments)
        text_parts = [content.text for content in result.content if hasattr(content, "text")]
        return "\n".join(text_parts) if text_parts else "No response"

    async def gui_list_resources(self):
        resources = await self.list_resources()
        if not resources:
            return "No resources available"
        return "\n\n".join(
            f"- {getattr(resource, 'name', 'Resource')}\n  URI template: {getattr(resource, 'uriTemplate', '')}"
            for resource in resources
        )

    async def gui_read_resource(self, uri: str):
        if not uri:
            return "Error: Please enter a resource URI"
        result = await self.read_resource(uri)
        text_parts = [content.text for content in result if hasattr(content, "text")]
        return "\n".join(text_parts) if text_parts else "No content"

    async def gui_list_prompts(self):
        import gradio as gr

        prompts = await self.list_prompts()
        output_lines = []
        choices = []
        for prompt in prompts:
            arg_names = [argument.name for argument in prompt.arguments] if prompt.arguments else []
            args_info = f" (args: {', '.join(arg_names)})" if arg_names else ""
            output_lines.append(f"- {prompt.name}: {prompt.description or 'Prompt'}{args_info}")
            choices.append(prompt.name)
        return "\n".join(output_lines), gr.update(choices=choices)

    async def gui_get_prompt(self, prompt_name: str, arguments_json: str):
        if not prompt_name:
            return "Error: Please select a prompt first"
        try:
            arguments = json.loads(arguments_json) if arguments_json else {}
        except json.JSONDecodeError:
            return "Error: Invalid JSON format"
        prompt = await self.get_prompt(prompt_name, arguments)
        output = [f"--- Prompt: {prompt.description or prompt_name} ---", ""]
        for message in prompt.messages:
            content = message.content.text if hasattr(message.content, "text") else str(message.content)
            output.append(f"{message.role}: {content}")
        return "\n".join(output)

    def create_interface(self):
        import gradio as gr

        with gr.Blocks(title="MCP HTTP Client") as interface:
            gr.Markdown("# MCP HTTP Client")
            gr.Markdown(
                f"**Server:** {self.server_url}\n\n"
                f"**Workspace Roots:** {self.roots_dir}\n\n"
                "This client connects through Streamable HTTP and declares filesystem roots."
            )

            with gr.Tabs():
                with gr.Tab("Tools"):
                    with gr.Row():
                        with gr.Column():
                            list_tools_btn = gr.Button("List Tools", variant="primary")
                            tools_output = gr.Textbox(label="Available Tools", lines=6)
                        with gr.Column():
                            tool_dropdown = gr.Dropdown(label="Select Tool", choices=[], interactive=True)
                            tool_args = gr.Textbox(label="Arguments", placeholder='{"directory": "."}', lines=3)
                            call_tool_btn = gr.Button("Call Tool", variant="primary")
                            tool_result = gr.Textbox(label="Tool Result", lines=10)
                    list_tools_btn.click(fn=self.gui_list_tools, outputs=[tools_output, tool_dropdown])
                    call_tool_btn.click(fn=self.gui_call_tool, inputs=[tool_dropdown, tool_args], outputs=tool_result)

                with gr.Tab("Resources"):
                    with gr.Row():
                        with gr.Column():
                            list_resources_btn = gr.Button("List Resource Templates", variant="primary")
                            resources_output = gr.Textbox(label="Resources", lines=6)
                        with gr.Column():
                            resource_uri = gr.Textbox(label="Resource URI", placeholder="file://workspace/test.txt")
                            read_resource_btn = gr.Button("Read Resource", variant="primary")
                            resource_content = gr.Textbox(label="Resource Content", lines=10)
                    list_resources_btn.click(fn=self.gui_list_resources, outputs=resources_output)
                    read_resource_btn.click(fn=self.gui_read_resource, inputs=resource_uri, outputs=resource_content)

                with gr.Tab("Prompts"):
                    with gr.Row():
                        with gr.Column():
                            list_prompts_btn = gr.Button("List Prompts", variant="primary")
                            prompts_output = gr.Textbox(label="Prompts", lines=6)
                        with gr.Column():
                            prompt_dropdown = gr.Dropdown(label="Select Prompt", choices=[], interactive=True)
                            prompt_args = gr.Textbox(label="Arguments", placeholder='{"filename": "example.py"}', lines=2)
                            get_prompt_btn = gr.Button("Get Prompt", variant="primary")
                            prompt_result = gr.Textbox(label="Prompt Result", lines=10)
                    list_prompts_btn.click(fn=self.gui_list_prompts, outputs=[prompts_output, prompt_dropdown])
                    get_prompt_btn.click(fn=self.gui_get_prompt, inputs=[prompt_dropdown, prompt_args], outputs=prompt_result)

        return interface


def main():
    if len(sys.argv) < 3:
        print("Usage: python advanced_http_client_app.py <server_url> <roots_dir>")
        sys.exit(1)
    client = MCPHTTPClientApp(sys.argv[1], sys.argv[2])
    interface = client.create_interface()
    interface.queue().launch(server_name="127.0.0.1", server_port=GUI_PORT)


if __name__ == "__main__":
    main()