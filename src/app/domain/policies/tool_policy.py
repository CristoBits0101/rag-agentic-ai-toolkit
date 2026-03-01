ALLOWED_TOOLS: set[str] = {"calculator", "database", "search"}


def is_tool_allowed(tool_name: str) -> bool:
    normalized = tool_name.strip().lower()
    return normalized in ALLOWED_TOOLS
