# --- DEPENDENCIAS ---
import json
import math
import os
import re
from urllib.parse import quote_plus
from urllib.request import urlopen

from config.react_agent_config import SEARCH_MAX_RESULTS


def build_tavily_tool(max_results: int = SEARCH_MAX_RESULTS):
    api_key = os.environ.get("TAVILY_API_KEY", "").strip()
    if not api_key:
        return None

    try:
        from langchain_community.tools.tavily_search import TavilySearchResults
    except Exception:
        return None

    try:
        return TavilySearchResults(max_results=max_results)
    except Exception:
        return None


def infer_city_from_query(query: str) -> str:
    match = re.search(r"in ([A-Za-z\s]+?)(?:\?|,| and|$)", query, flags=re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return "Zurich"


def search_weather_fallback(query: str):
    city = infer_city_from_query(query)
    url = f"https://wttr.in/{quote_plus(city)}?format=j1"
    with urlopen(url, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))

    current = payload.get("current_condition", [{}])[0]
    description = current.get("weatherDesc", [{}])[0].get("value", "Unknown")
    return [
        {
            "title": f"Current weather in {city}",
            "url": f"https://wttr.in/{quote_plus(city)}",
            "content": (
                f"Weather: {description}. Temperature C: {current.get('temp_C', 'NA')}. "
                f"Feels like C: {current.get('FeelsLikeC', 'NA')}. Humidity: {current.get('humidity', 'NA')}."
            ),
            "source": "wttr.in",
        }
    ]


def search_duckduckgo_fallback(query: str, max_results: int = SEARCH_MAX_RESULTS):
    url = f"https://api.duckduckgo.com/?q={quote_plus(query)}&format=json&no_html=1&skip_disambig=1"
    with urlopen(url, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))

    results = []
    if payload.get("AbstractText"):
        results.append(
            {
                "title": payload.get("Heading", query),
                "url": payload.get("AbstractURL", "https://duckduckgo.com/"),
                "content": payload.get("AbstractText", ""),
                "source": "duckduckgo",
            }
        )

    for topic in payload.get("RelatedTopics", []):
        if len(results) >= max_results:
            break
        if isinstance(topic, dict) and topic.get("Text"):
            results.append(
                {
                    "title": topic.get("Text", query)[:80],
                    "url": topic.get("FirstURL", "https://duckduckgo.com/"),
                    "content": topic.get("Text", ""),
                    "source": "duckduckgo",
                }
            )
        elif isinstance(topic, dict) and topic.get("Topics"):
            for nested in topic.get("Topics", []):
                if len(results) >= max_results:
                    break
                if nested.get("Text"):
                    results.append(
                        {
                            "title": nested.get("Text", query)[:80],
                            "url": nested.get("FirstURL", "https://duckduckgo.com/"),
                            "content": nested.get("Text", ""),
                            "source": "duckduckgo",
                        }
                    )

    return results


SAFE_BIN_OPS = {
    "Add": lambda left, right: left + right,
    "Sub": lambda left, right: left - right,
    "Mult": lambda left, right: left * right,
    "Div": lambda left, right: left / right,
    "Pow": lambda left, right: left**right,
    "Mod": lambda left, right: left % right,
}

SAFE_UNARY_OPS = {
    "UAdd": lambda value: +value,
    "USub": lambda value: -value,
}

SAFE_MATH_FUNCS = {
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log,
    "log10": math.log10,
    "exp": math.exp,
    "abs": abs,
    "round": round,
}

SAFE_CONSTANTS = {
    "pi": math.pi,
    "e": math.e,
}