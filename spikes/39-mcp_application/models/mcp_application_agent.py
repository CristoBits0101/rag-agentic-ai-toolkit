# --- DEPENDENCIAS ---
from config.mcp_application_config import AGENT_INTRO


class SessionPersistentMcpAgent:
    def __init__(self, tools: list):
        self.tools = {tool.name: tool for tool in tools}
        self.history: list[dict[str, str]] = []

    def introduce(self) -> str:
        tool_names = ", ".join(sorted(self.tools))
        intro = f"{AGENT_INTRO} Available tools: {tool_names}."
        self.history.append({"role": "assistant", "content": intro})
        return intro

    async def ask(self, query: str) -> str:
        self.history.append({"role": "user", "content": query})
        lowered = query.lower()
        if "remember" in lowered or "previous" in lowered:
            answer = f"I currently remember {len(self.history) - 1} prior messages in this session."
            self.history.append({"role": "assistant", "content": answer})
            return answer
        if any(word in lowered for word in ["fastmcp", "documentation", "library"]):
            resolve_text = await self.tools["resolve-library-id"].ainvoke({"libraryName": "fastmcp", "query": query})
            docs_text = await self.tools["query-docs"].ainvoke(
                {
                    "libraryId": "/llmstxt/gofastmcp_llms-full_txt",
                    "query": query,
                    "tokens": 1200,
                }
            )
            answer = f"Documentation lookup completed.\n{resolve_text}\n\n{docs_text}"
            self.history.append({"role": "assistant", "content": answer})
            return answer
        if any(word in lowered for word in ["museum", "met", "art", "painting", "van gogh", "hokusai"]):
            search_text = await self.tools["search-met-art"].ainvoke({"query": query})
            first_line = search_text.splitlines()[0]
            object_id = int(first_line.split(":", 1)[0].replace("-", "").strip())
            details = await self.tools["get-artwork-details"].ainvoke({"object_id": object_id})
            answer = f"Museum lookup completed.\n{search_text}\n\n{details}"
            self.history.append({"role": "assistant", "content": answer})
            return answer
        answer = "I can help with FastMCP documentation or with Met Museum collection lookups."
        self.history.append({"role": "assistant", "content": answer})
        return answer
