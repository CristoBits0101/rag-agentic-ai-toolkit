# --- DEPENDENCIAS ---
import asyncio
import json
import re
import sys
from contextlib import AsyncExitStack
from urllib.parse import quote

from fastmcp import Client
from fastmcp.client.elicitation import ElicitResult

from models.local_mcp_assistant import build_code_review
from models.local_mcp_assistant import build_documentation_markdown
from models.local_mcp_assistant import summarize_directory_payload


class MCPClient:
    def __init__(self, scripted_inputs: list[str] | None = None):
        self.exit_stack = AsyncExitStack()
        self.client = None
        self.scripted_inputs = list(scripted_inputs or [])
        self.progress_log: list[str] = []
        self.notifications: list[str] = []

    def _read_console(self, prompt: str) -> str:
        if self.scripted_inputs:
            return self.scripted_inputs.pop(0)
        return input(prompt)

    async def connect_to_server(self, server_script_path: str):
        if not server_script_path.endswith((".py", ".js", ".ts")):
            raise ValueError("Server script must be a .py, .js, or .ts file")
        self.client = Client(
            server_script_path,
            elicitation_handler=self.handle_elicitation,
            progress_handler=self.handle_progress,
            message_handler=self.handle_message,
        )
        await self.exit_stack.enter_async_context(self.client)

    async def handle_elicitation(self, message: str, response_type: type, params, context):
        print(f"Server asks: {message}")
        user_data = {}
        for field_name, field_type in response_type.__annotations__.items():
            field_type_name = getattr(field_type, "__name__", str(field_type))
            user_input = self._read_console(f"Enter value for '{field_name}' ({field_type_name}): ").strip()
            if not user_input:
                return ElicitResult(action="decline")
            user_data[field_name] = user_input
        return response_type(**user_data)

    async def handle_progress(self, progress: float, total: float | None, message: str | None) -> None:
        if total is not None and total:
            percentage = (progress / total) * 100
            line = f"Progress: {percentage:.1f}% - {message or ''}"
        else:
            line = f"Progress: {progress} - {message or ''}"
        self.progress_log.append(line)
        print(line)

    async def handle_message(self, message):
        if hasattr(message, "root"):
            method = message.root.method
            self.notifications.append(method)
            print(f"Received: {method}")

    async def _get_tools(self):
        tools_response = await self.client.list_tools()
        return [
            {
                "name": tool.name,
                "description": tool.description or "MCP Tool",
                "input_schema": tool.inputSchema,
            }
            for tool in tools_response
        ]

    async def _get_prompts(self):
        return await self.client.list_prompts()

    async def _get_resources(self):
        return await self.client.list_resources()

    async def _get_resource_templates(self):
        return await self.client.list_resource_templates()

    async def process_query(self, query: str) -> str:
        lowered = query.lower()
        if query.startswith("You are an expert code editor"):
            return build_code_review(query)
        if query.startswith("You are an expert technical writer"):
            doc_name, markdown = build_documentation_markdown(query)
            result = await self.client.call_tool("write_file", {"file_path": doc_name, "content": markdown})
            return f"{result.content[0].text}\nDocumentation file: {doc_name}"
        if "directory" in lowered:
            resource = await self.client.read_resource("dir://.")
            return summarize_directory_payload(resource[0].text)
        if "tool" in lowered:
            tools = await self._get_tools()
            return "Available tools: " + ", ".join(tool["name"] for tool in tools)
        return "This local assistant can review code generate documentation list directories and call MCP file tools."

    async def converse(self):
        print("\nEntering conversation mode. Type 'quit' or 'q' to exit.")
        while True:
            query = self._read_console("\nQuery: ").strip()
            if query.lower() in ("quit", "q"):
                break
            if not query:
                print("Please enter a query")
                continue
            print("\n" + await self.process_query(query))

    async def prompt(self, prompt_name: str, arguments: dict | None = None):
        prompts_response = await self._get_prompts()
        prompt_obj = next((prompt for prompt in prompts_response if prompt.name == prompt_name), None)
        if prompt_obj is None:
            raise ValueError(f"Prompt '{prompt_name}' not found")
        resolved_arguments = dict(arguments or {})
        if prompt_obj.arguments and not arguments:
            for argument in prompt_obj.arguments:
                label = "required" if argument.required else "optional"
                user_input = self._read_console(f"{argument.name} ({label}): ").strip()
                if not user_input and argument.required:
                    raise ValueError(f"Error: {argument.name} is required")
                if user_input:
                    resolved_arguments[argument.name] = user_input
        prompt_result = await self.client.get_prompt(prompt_name, arguments=resolved_arguments)
        prompt = prompt_result.messages[0].content.text
        response = await self.process_query(prompt)
        print(response)
        return response

    async def read_file(self, file_name: str | None = None):
        selected = file_name or self._read_console("Enter file path: ").strip()
        encoded_file_name = quote(selected, safe="")
        resource = await self.client.read_resource(f"file:///{encoded_file_name}")
        payload = json.loads(resource[0].text)
        file_content = payload.get("file_content") or payload.get("error", "")
        print(f"File Content:\n {file_content}")
        return file_content

    def _print_dir_listing(self, items: list[dict]):
        print("\nDirectory Listing:\n")
        print(f"{'Type':<10} {'Size':>10} {'Modified':<25} {'Name'}")
        print("-" * 70)
        for item in items:
            type_icon = "[D]" if item["type"] == "directory" else "[F]"
            size = f"{item['size']} B"
            print(f"{type_icon:<3} {item['type']:<8} {size:>10}  {item['modified']:<25} {item['name']}")

    async def read_dir(self):
        resource = await self.client.read_resource("dir://.")
        dir_list = json.loads(resource[0].text)["items"]
        self._print_dir_listing(dir_list)
        return dir_list

    async def menu(self):
        print("\nMCP Client Started!")
        print("Select from the menu or 'quit' or 'q' to exit.")
        menu_actions = {
            "1": lambda: self.prompt("documentation_generator"),
            "2": lambda: self.prompt("code_review"),
            "3": self.read_file,
            "4": self.read_dir,
            "5": self.converse,
            "q": self.quit_action,
            "quit": self.quit_action,
        }
        while True:
            choice = self._read_console(
                """
Select from the Menu
1. Generate Documentation
2. Review Code
3. Read File
4. Read Current Directory
5. Converse with Agent
q. Quit
> """
            ).strip()
            action = menu_actions.get(choice)
            if not action:
                print("Invalid choice. Please try again.")
                continue
            result = await action()
            if result == "quit":
                break

    async def quit_action(self):
        print("Exiting client...")
        return "quit"

    async def cleanup(self):
        if self.exit_stack:
            await self.exit_stack.aclose()


async def main():
    if len(sys.argv) < 2:
        print("Usage: python client.py <server_path>")
        sys.exit(1)
    client = MCPClient()
    try:
        await client.connect_to_server(sys.argv[1])
        await client.menu()
    finally:
        await client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
