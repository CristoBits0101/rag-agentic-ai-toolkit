# --- DEPENDENCIAS ---
import ast
import json
import re
from typing import Any

from langchain_core.tools import BaseTool
from langchain_core.tools import tool

from models.react_search_gateway import SAFE_BIN_OPS
from models.react_search_gateway import SAFE_CONSTANTS
from models.react_search_gateway import SAFE_MATH_FUNCS
from models.react_search_gateway import SAFE_UNARY_OPS
from models.react_search_gateway import build_tavily_tool
from models.react_search_gateway import search_duckduckgo_fallback
from models.react_search_gateway import search_hacker_news_fallback
from models.react_search_gateway import search_weather_fallback


def normalize_weather_text(weather: str) -> str:
    return " ".join(weather.lower().split())


@tool
def search_tool(query: str) -> list[dict[str, str]]:
    """
    Search for current information using Tavily when available.

    Falls back to Open Meteo for weather queries, HN Algolia for news queries, and DuckDuckGo Instant Answer for general queries.
    """
    normalized_query = query.strip()
    if not normalized_query:
        return []

    tavily_tool = build_tavily_tool()
    if tavily_tool is not None:
        try:
            return tavily_tool.invoke(normalized_query)
        except Exception:
            pass

    if "weather" in normalized_query.lower():
        try:
            return search_weather_fallback(normalized_query)
        except Exception:
            return []

    if "news" in normalized_query.lower() or "recent ai" in normalized_query.lower() or "latest ai" in normalized_query.lower():
        try:
            return search_hacker_news_fallback(normalized_query)
        except Exception:
            pass

    try:
        return search_duckduckgo_fallback(normalized_query)
    except Exception:
        return []


@tool
def recommend_clothing(weather: str) -> str:
    """
    Return a clothing recommendation based on the provided weather description.
    """
    normalized_weather = normalize_weather_text(weather)
    if "snow" in normalized_weather or "freezing" in normalized_weather:
        return "Wear a heavy coat, gloves, and boots."
    if "rain" in normalized_weather or "wet" in normalized_weather:
        return "Bring a raincoat and waterproof shoes."
    if "hot" in normalized_weather or "85" in normalized_weather:
        return "T-shirt, shorts, and sunscreen recommended."
    if "cold" in normalized_weather or "50" in normalized_weather or "temp c: 10" in normalized_weather:
        return "Wear a warm jacket or sweater."
    return "A light jacket should be fine."


def evaluate_ast_node(node):
    if isinstance(node, ast.Expression):
        return evaluate_ast_node(node.body)

    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value

    if isinstance(node, ast.BinOp):
        operator_name = type(node.op).__name__
        if operator_name not in SAFE_BIN_OPS:
            raise ValueError("Unsupported binary operator.")
        return SAFE_BIN_OPS[operator_name](evaluate_ast_node(node.left), evaluate_ast_node(node.right))

    if isinstance(node, ast.UnaryOp):
        operator_name = type(node.op).__name__
        if operator_name not in SAFE_UNARY_OPS:
            raise ValueError("Unsupported unary operator.")
        return SAFE_UNARY_OPS[operator_name](evaluate_ast_node(node.operand))

    if isinstance(node, ast.Name):
        if node.id not in SAFE_CONSTANTS:
            raise ValueError("Unsupported identifier.")
        return SAFE_CONSTANTS[node.id]

    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        function_name = node.func.id
        if function_name not in SAFE_MATH_FUNCS:
            raise ValueError("Unsupported function.")
        arguments = [evaluate_ast_node(argument) for argument in node.args]
        return SAFE_MATH_FUNCS[function_name](*arguments)

    raise ValueError("Unsafe or unsupported expression.")


def prepare_expression(expression: str) -> str:
    normalized_expression = expression.strip().lower()
    normalized_expression = normalized_expression.replace("π", "pi")
    normalized_expression = normalized_expression.replace("^", "**")
    normalized_expression = normalized_expression.replace("divided by", "/")
    normalized_expression = normalized_expression.replace("multiplied by", "*")
    normalized_expression = normalized_expression.replace("times", "*")
    normalized_expression = normalized_expression.replace("plus", "+")
    normalized_expression = normalized_expression.replace("minus", "-")
    normalized_expression = re.sub(r"(\d+(?:\.\d+)?)\s*%\s*of\s*(\d+(?:\.\d+)?)", r"(\1/100) * \2", normalized_expression)
    normalized_expression = re.sub(r"square root of\s*([\d\.]+)", r"sqrt(\1)", normalized_expression)
    return normalized_expression


@tool
def calculator_tool(expression: str) -> str:
    """
    Safely evaluate mathematical expressions such as arithmetic sqrt and trigonometric functions.
    """
    try:
        parsed_expression = ast.parse(prepare_expression(expression), mode="eval")
        result = evaluate_ast_node(parsed_expression)
    except Exception as exc:
        return f"Could not evaluate expression: {exc}"

    if float(result).is_integer():
        return str(int(result))
    return str(round(float(result), 6))


@tool
def news_summarizer_tool(news_content: str) -> str:
    """
    Summarize raw search results or news content into up to three concise bullet summaries.
    """
    try:
        parsed_content = json.loads(news_content)
    except Exception:
        parsed_content = None

    articles = []
    if isinstance(parsed_content, list):
        articles = parsed_content
    elif isinstance(parsed_content, dict):
        for key, value in parsed_content.items():
            if isinstance(value, list):
                articles.extend(value)

    if not articles:
        articles = [{"title": "Summary", "content": news_content, "url": ""}]

    lines = []
    for index, article in enumerate(articles[:3], start=1):
        title = str(article.get("title", "Untitled article")).strip()
        url = str(article.get("url", "")).strip()
        content = str(article.get("content", article.get("snippet", ""))).strip()
        content = " ".join(content.split())
        short_content = content[:220] + ("..." if len(content) > 220 else "")
        lines.append(f"{index}. {title}: {short_content} {url}".strip())

    return "\n".join(lines)


def build_react_tools() -> list[BaseTool]:
    return [
        search_tool,
        recommend_clothing,
        calculator_tool,
        news_summarizer_tool,
    ]


def build_tools_by_name(tools: list[BaseTool] | None = None) -> dict[str, BaseTool]:
    selected_tools = tools or build_react_tools()
    return {tool.name: tool for tool in selected_tools}


def describe_tool_schemas(tools: list[BaseTool] | None = None) -> list[dict[str, Any]]:
    selected_tools = tools or build_react_tools()
    return [
        {
            "name": tool.name,
            "description": tool.description,
            "args": tool.args,
        }
        for tool in selected_tools
    ]