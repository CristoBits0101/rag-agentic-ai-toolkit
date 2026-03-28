# --- DEPENDENCIAS ---
import re
import sys
from pathlib import Path

SPIKE_ROOT = Path(__file__).resolve().parents[1]
if str(SPIKE_ROOT) not in sys.path:
    sys.path.insert(0, str(SPIKE_ROOT))

from config.advanced_mcp_http_config import HOST_PORT
from models.advanced_http_client_base import MCPHTTPClient


class MCPHTTPHostApp(MCPHTTPClient):
    """Deterministic host app that uses MCP tools over HTTP."""

    def __init__(self, server_url: str, roots_dir: str):
        super().__init__(server_url, roots_dir)
        self.conversation_history: list[dict[str, str]] = []
        self.mode = "local-deterministic-host"

    async def execute_tool(self, tool_name: str, arguments: dict) -> str:
        if tool_name == "mcp_list_resources":
            resources = await self.list_resources()
            lines = ["Available resources:"]
            for resource in resources:
                lines.append(f"- {getattr(resource, 'uriTemplate', '')}")
            return "\n".join(lines)
        if tool_name == "mcp_read_resource":
            uri = arguments.get("uri", "")
            contents = await self.read_resource(uri)
            return "\n".join(content.text for content in contents if hasattr(content, "text"))
        if tool_name == "mcp_list_prompts":
            prompts = await self.list_prompts()
            lines = ["Available prompts:"]
            for prompt in prompts:
                arg_names = [argument.name for argument in prompt.arguments] if prompt.arguments else []
                suffix = f" (args: {', '.join(arg_names)})" if arg_names else ""
                lines.append(f"- {prompt.name}{suffix}")
            return "\n".join(lines)
        if tool_name == "mcp_get_prompt":
            prompt_name = arguments.get("name", "")
            prompt_args = arguments.get("arguments", {})
            prompt = await self.get_prompt(prompt_name, prompt_args)
            return "\n".join(
                f"{message.role}: {message.content.text if hasattr(message.content, 'text') else str(message.content)}"
                for message in prompt.messages
            )
        result = await self.call_tool(tool_name, arguments)
        text_parts = [content.text for content in result.content if hasattr(content, "text")]
        return "\n".join(text_parts) if text_parts else str(result)

    async def ask(self, query: str) -> str:
        self.conversation_history.append({"role": "user", "content": query})
        lowered = query.lower().strip()

        create_match = re.search(
            r"create (?:a )?file called ([\w./-]+) with (?:the message|content)[: ]+(.+)",
            query,
            re.IGNORECASE,
        )
        if create_match:
            filepath = create_match.group(1)
            content = create_match.group(2).strip().strip('"')
            result = await self.execute_tool("write_file", {"filepath": filepath, "content": content})
            answer = f"I created {filepath}.\n{result}"
        elif lowered.startswith("read the file") or lowered.startswith("read file"):
            filepath = query.split()[-1]
            answer = await self.execute_tool("read_file", {"filepath": filepath})
        elif "what resources" in lowered:
            listing = await self.execute_tool("mcp_list_resources", {})
            resource_text = await self.execute_tool("mcp_read_resource", {"uri": "file://workspace/test.txt"})
            answer = f"{listing}\n\nRead file://workspace/test.txt:\n{resource_text}"
        elif "prompt" in lowered and "review_code" in lowered:
            answer = await self.execute_tool("mcp_get_prompt", {"name": "review_code", "arguments": {"filename": "example.py"}})
        elif "root" in lowered or "boundary" in lowered:
            answer = await self.execute_tool("list_roots_boundary", {})
        elif "analyze this code" in lowered:
            code = query.split(":", 1)[1].strip() if ":" in query else query
            answer = await self.execute_tool("analyze_code", {"code": code, "focus": "security"})
        else:
            answer = "I can create files read workspace content inspect roots and trigger sampling based analysis."

        self.conversation_history.append({"role": "assistant", "content": answer})
        return answer

    def create_interface(self):
        import gradio as gr

        async def chat_wrapper(message, history):
            if not message.strip():
                return history
            response = await self.ask(message)
            return history + [{"role": "user", "content": message}, {"role": "assistant", "content": response}]

        async def clear_history():
            self.conversation_history = []
            return []

        with gr.Blocks(title="MCP HTTP Host") as interface:
            gr.Markdown(
                f"# MCP HTTP Host\n\n**Server:** {self.server_url}\n\n**Roots:** {self.roots_dir}\n\n"
                f"**Mode:** {self.mode}"
            )
            chatbot = gr.Chatbot(label="Conversation", height=500, type="messages")
            with gr.Row():
                message = gr.Textbox(label="Your message", placeholder="Ask me to use MCP tools", scale=4)
                clear = gr.Button("Clear", scale=1)
            message.submit(fn=chat_wrapper, inputs=[message, chatbot], outputs=chatbot).then(lambda: "", outputs=message)
            clear.click(fn=clear_history, outputs=chatbot)
        return interface


def main():
    if len(sys.argv) < 3:
        print("Usage: python advanced_http_host_app.py <server_url> <roots_dir>")
        sys.exit(1)
    app = MCPHTTPHostApp(sys.argv[1], sys.argv[2])
    interface = app.create_interface()
    interface.queue().launch(server_name="127.0.0.1", server_port=HOST_PORT)


if __name__ == "__main__":
    main()