# --- DEPENDENCIAS ---
from dataclasses import dataclass
import re
from typing import Any
from typing import Callable

from config.daily_dish_chatbot_config import FAQ_ENTRIES
from config.daily_dish_chatbot_config import WEB_SNIPPETS


def _tokenize(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def _score_entry(query: str, keywords: list[str], title: str) -> float:
    query_tokens = _tokenize(query)
    keyword_tokens = set()
    for keyword in keywords:
        keyword_tokens.update(_tokenize(keyword))
    title_tokens = _tokenize(title)
    overlap = len(query_tokens & keyword_tokens)
    title_overlap = len(query_tokens & title_tokens)
    return float(overlap * 2 + title_overlap)


class LocalFaqSearchTool:
    name = "faq_search_tool"
    description = "Search the Daily Dish FAQ knowledge base for restaurant specific answers."

    def run(self, query: str) -> dict[str, Any]:
        best_entry = None
        best_score = -1.0
        for entry in FAQ_ENTRIES:
            score = _score_entry(query, entry["keywords"], entry["question"])
            if score > best_score:
                best_score = score
                best_entry = entry

        if best_entry is None:
            return {"tool": self.name, "found": False, "answer": "No FAQ answer was found.", "score": 0.0}

        return {
            "tool": self.name,
            "found": best_score > 0,
            "question": best_entry["question"],
            "answer": best_entry["answer"],
            "score": best_score,
        }


class LocalWebSearchTool:
    name = "web_search_tool"
    description = "Search local supplemental web snippets for parking transit and website details."

    def run(self, query: str) -> dict[str, Any]:
        best_entry = None
        best_score = -1.0
        for entry in WEB_SNIPPETS:
            score = _score_entry(query, entry["keywords"], entry["title"])
            if score > best_score:
                best_score = score
                best_entry = entry

        if best_entry is None:
            return {"tool": self.name, "found": False, "answer": "No supplemental web answer was found.", "score": 0.0}

        return {
            "tool": self.name,
            "found": best_score > 0,
            "title": best_entry["title"],
            "answer": best_entry["answer"],
            "score": best_score,
        }


@dataclass
class FunctionTool:
    name: str
    description: str
    fn: Callable[[str], Any]

    def run(self, data: str):
        return self.fn(data)


def tool(name: str):
    def decorator(fn: Callable[[str], Any]):
        description = (fn.__doc__ or "").strip()
        return FunctionTool(name=name, description=description, fn=fn)

    return decorator


@tool("Add Two Numbers Tool")
def add_numbers(data: str) -> int:
    """Extract integers from text and return their sum."""
    numbers = list(map(int, re.findall(r"-?\d+", data)))
    return sum(numbers)


@tool("Multiply Numbers Tool")
def multiply_numbers(data: str) -> int:
    """Extract integers from text and return their product."""
    numbers = list(map(int, re.findall(r"-?\d+", data)))
    product = 1
    for number in numbers:
        product *= number
    return product