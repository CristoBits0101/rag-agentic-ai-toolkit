# --- DEPENDENCIAS ---
from pathlib import Path

from client import MCPClient
from config.enhanced_mcp_config import SAMPLE_CODE
from config.enhanced_mcp_config import SAMPLE_FILE
from config.enhanced_mcp_config import SPIKE_ROOT


async def run_enhanced_mcp_demo() -> dict[str, object]:
    server_path = str(SPIKE_ROOT / "server.py")
    client = MCPClient(scripted_inputs=[SAMPLE_FILE, "sample_subject_docs"])
    try:
        await client.connect_to_server(server_path)
        await client.client.call_tool("write_file", {"file_path": SAMPLE_FILE, "content": SAMPLE_CODE})
        directory_items = await client.read_dir()
        file_content = await client.read_file(SAMPLE_FILE)
        review_output = await client.prompt("code_review", {"file_path": SAMPLE_FILE})
        documentation_output = await client.prompt("documentation_generator")
        conversation_output = await client.process_query("List the tools and summarize the current directory.")
        generated_doc = Path(SPIKE_ROOT / "sample_subject_docs.md")
        generated_text = generated_doc.read_text(encoding="utf-8") if generated_doc.exists() else ""
        return {
            "directory_count": len(directory_items),
            "file_content": file_content,
            "review_output": review_output,
            "documentation_output": documentation_output,
            "conversation_output": conversation_output,
            "generated_text": generated_text,
            "progress_log": list(client.progress_log),
        }
    finally:
        await client.cleanup()
