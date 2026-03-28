# --- DEPENDENCIAS ---
from pathlib import Path

SPIKE_ROOT = Path(__file__).resolve().parents[1]
HTTP_HOST = "127.0.0.1"
HTTP_PORT = 8938
REAL_CONTEXT7_URL = "https://mcp.context7.com/mcp"
REAL_CONTEXT7_NPX_PACKAGE = "@upstash/context7-mcp"
LIBRARY_CATALOG = {
    "/llmstxt/gofastmcp_llms-full_txt": {
        "title": "FastMCP",
        "description": "FastMCP is a Python framework for building MCP servers with tools resources prompts and HTTP or STDIO transports.",
        "snippets": 12289,
        "source_reputation": "High",
        "benchmark_score": 79,
        "trust_score": 9.6,
        "body": (
            "FastMCP quick reference:\n"
            "- Create a server with FastMCP('name').\n"
            "- Register tools with @mcp.tool.\n"
            "- Register resources with @mcp.resource.\n"
            "- Register prompts with @mcp.prompt.\n"
            "- Run local STDIO servers with mcp.run().\n"
            "- Run HTTP servers with await mcp.run_http_async().\n"
            "- Connect clients with Client transport objects such as StdioTransport and StreamableHttpTransport.\n"
            "- Use async with Client(...) as client then await client.list_tools() or await client.call_tool(...).\n"
        ),
    },
    "/scikit-learn/scikit-learn": {
        "title": "scikit-learn",
        "description": "Scikit-learn offers classical machine learning algorithms model selection and preprocessing utilities for Python.",
        "snippets": 9800,
        "source_reputation": "High",
        "benchmark_score": 76,
        "trust_score": 9.4,
        "body": (
            "scikit-learn quick reference:\n"
            "- Use train_test_split for train and validation splits.\n"
            "- Use Pipeline to combine preprocessing and estimators.\n"
            "- Common estimators include LogisticRegression RandomForestClassifier and LinearRegression.\n"
        ),
    },
}
