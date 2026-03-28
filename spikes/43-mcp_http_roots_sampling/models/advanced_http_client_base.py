# --- DEPENDENCIAS ---
from contextlib import AsyncExitStack
from pathlib import Path

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from mcp.types import CreateMessageResult
from mcp.types import ListRootsResult
from mcp.types import Root
from mcp.types import TextContent

from config.advanced_mcp_http_config import HTTP_PATH


class MCPHTTPClient:
    """Base MCP HTTP client with roots and sampling support."""

    def __init__(self, server_url: str, roots_dir: str | Path):
        self.server_url = server_url.rstrip("/")
        self.roots_dir = Path(roots_dir).resolve()
        self.roots_dir.mkdir(parents=True, exist_ok=True)
        self.session = None
        self.exit_stack = AsyncExitStack()
        self._connected = False
        self.sampling_requests: list[dict[str, str | int]] = []
        self.roots_requests = 0

    def _build_roots(self) -> list[Root]:
        return [Root(uri=self.roots_dir.as_uri(), name="Workspace")]

    async def _handle_list_roots(self, _context) -> ListRootsResult:
        self.roots_requests += 1
        return ListRootsResult(roots=self._build_roots())

    async def _handle_sampling(self, _context, params) -> CreateMessageResult:
        joined_messages = []
        for message in params.messages:
            content = message.content
            if hasattr(content, "text"):
                joined_messages.append(content.text)
            else:
                joined_messages.append(str(content))
        prompt_text = "\n".join(joined_messages)
        lowered = prompt_text.lower()
        focus = "security" if "security" in lowered else "quality"
        findings: list[str] = []
        if "def " in prompt_text:
            findings.append("The snippet defines at least one function and is easy to follow.")
        if "return" in prompt_text:
            findings.append("Return paths are explicit and easy to trace.")
        if "eval(" in prompt_text or "exec(" in prompt_text:
            findings.append("Avoid dynamic evaluation in production code because it expands attack surface.")
        if not findings:
            findings.append("No critical issues were detected in the provided snippet.")
        findings.append(f"Focus: {focus}.")
        response_text = " ".join(findings)
        self.sampling_requests.append(
            {
                "prompt": prompt_text[:400],
                "focus": focus,
                "max_tokens": params.maxTokens,
            }
        )
        return CreateMessageResult(
            role="assistant",
            content=TextContent(type="text", text=response_text),
            model="local-deterministic-sampling",
            stopReason="endTurn",
        )

    async def connect(self):
        if self._connected:
            return
        mcp_url = f"{self.server_url}{HTTP_PATH}"
        read, write, _ = await self.exit_stack.enter_async_context(streamablehttp_client(mcp_url))
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(
                read,
                write,
                sampling_callback=self._handle_sampling,
                list_roots_callback=self._handle_list_roots,
            )
        )
        await self.session.initialize()
        self._connected = True

    async def list_tools(self):
        await self.connect()
        result = await self.session.list_tools()
        return result.tools

    async def call_tool(self, tool_name: str, arguments: dict):
        await self.connect()
        return await self.session.call_tool(tool_name, arguments)

    async def list_resources(self):
        await self.connect()
        result = await self.session.list_resource_templates()
        return result.resourceTemplates

    async def read_resource(self, uri: str):
        await self.connect()
        result = await self.session.read_resource(uri)
        return result.contents

    async def list_prompts(self):
        await self.connect()
        result = await self.session.list_prompts()
        return result.prompts

    async def get_prompt(self, prompt_name: str, arguments: dict):
        await self.connect()
        return await self.session.get_prompt(prompt_name, arguments)

    def describe_roots(self) -> str:
        return "\n".join(f"- {root.name or 'Workspace'}: {root.uri}" for root in self._build_roots())

    async def cleanup(self):
        await self.exit_stack.aclose()