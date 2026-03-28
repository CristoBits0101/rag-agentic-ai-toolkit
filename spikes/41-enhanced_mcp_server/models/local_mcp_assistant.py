# --- DEPENDENCIAS ---
import json
import re


def build_code_review(prompt: str) -> str:
    file_match = re.search(r"File: (.+)", prompt)
    code_match = re.search(r"Current code:\n'''\n(.*?)\n'''", prompt, re.DOTALL)
    file_path = file_match.group(1) if file_match else "unknown"
    code = code_match.group(1).strip() if code_match else ""
    line_count = len([line for line in code.splitlines() if line.strip()])
    return (
        f"Code review for {file_path}.\n"
        f"- The file has {line_count} meaningful lines.\n"
        f"- The implementation is clear and compact.\n"
        f"- Consider adding docstrings and edge case tests if the function grows."
    )


def build_documentation_markdown(prompt: str) -> tuple[str, str]:
    file_match = re.search(r"File: (.+)", prompt)
    code_match = re.search(r"Current code:\n'''\n(.*?)\n'''", prompt, re.DOTALL)
    name_match = re.search(r"Name that separate document EXACTLY: (.+?)\*\*", prompt)
    file_path = file_match.group(1) if file_match else "unknown"
    code = code_match.group(1).strip() if code_match else ""
    raw_name = name_match.group(1).strip() if name_match else "documentation"
    doc_name = raw_name if raw_name.endswith(".md") else f"{raw_name}.md"
    markdown = (
        f"# Documentation for {file_path}\n\n"
        f"## Summary\n\n"
        f"This file contains executable Python code that can be served through the MCP workflow.\n\n"
        f"## Source\n\n"
        f"```python\n{code}\n```\n"
    )
    return doc_name, markdown


def summarize_directory_payload(resource_text: str) -> str:
    payload = json.loads(resource_text)
    items = payload.get("items", [])
    names = ", ".join(item["name"] for item in items[:8])
    return f"Current directory items: {names}."
