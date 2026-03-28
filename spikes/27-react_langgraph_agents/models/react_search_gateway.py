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
    geocoding_url = (
        "https://geocoding-api.open-meteo.com/v1/search"
        f"?name={quote_plus(city)}&count=1&language=en&format=json"
    )
    with urlopen(geocoding_url, timeout=30) as response:
        geocoding_payload = json.loads(response.read().decode("utf-8"))

    result = geocoding_payload.get("results", [{}])[0]
    latitude = result.get("latitude")
    longitude = result.get("longitude")
    if latitude is None or longitude is None:
        raise ValueError("Could not geocode city.")

    forecast_url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}&longitude={longitude}&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code"
    )
    with urlopen(forecast_url, timeout=30) as response:
        forecast_payload = json.loads(response.read().decode("utf-8"))

    current = forecast_payload.get("current", {})
    return [
        {
            "title": f"Current weather in {city}",
            "url": "https://open-meteo.com/",
            "content": (
                f"Weather code: {current.get('weather_code', 'NA')}. Temperature C: {current.get('temperature_2m', 'NA')}. "
                f"Feels like C: {current.get('apparent_temperature', 'NA')}. Humidity: {current.get('relative_humidity_2m', 'NA')}."
            ),
            "source": "open_meteo",
        }
    ]


def search_hacker_news_fallback(query: str, max_results: int = SEARCH_MAX_RESULTS):
    url = f"https://hn.algolia.com/api/v1/search?tags=story&hitsPerPage={max_results}&query={quote_plus(query)}"
    with urlopen(url, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))

    results = []
    for hit in payload.get("hits", [])[:max_results]:
        title = str(hit.get("title") or hit.get("story_title") or query).strip()
        story_url = str(hit.get("url") or hit.get("story_url") or "https://news.ycombinator.com/").strip()
        story_text = str(hit.get("story_text") or hit.get("comment_text") or "No summary available.").strip()
        results.append(
            {
                "title": title,
                "url": story_url,
                "content": story_text,
                "source": "hn_algolia",
            }
        )

    return results


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