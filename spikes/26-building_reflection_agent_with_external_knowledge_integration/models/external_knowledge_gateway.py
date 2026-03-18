# --- DEPENDENCIAS ---
import json
import os
from dataclasses import dataclass
from urllib.parse import quote_plus
from urllib.request import urlopen

from config.external_reflection_agent_config import SEARCH_MAX_RESULTS


@dataclass(frozen=True)
class SearchDocument:
    title: str
    url: str
    snippet: str
    source: str


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


def normalize_tavily_results(raw_result) -> list[SearchDocument]:
    if not isinstance(raw_result, list):
        return []

    documents = []
    for item in raw_result:
        if not isinstance(item, dict):
            continue
        documents.append(
            SearchDocument(
                title=str(item.get("title", "")).strip(),
                url=str(item.get("url", "")).strip(),
                snippet=str(item.get("content", "")).strip(),
                source="tavily",
            )
        )
    return documents


def build_pubmed_url(record: dict) -> str:
    pmid = str(record.get("pmid", "")).strip()
    if pmid:
        return f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"

    identifier = str(record.get("id", "")).strip()
    if identifier:
        return f"https://europepmc.org/article/MED/{identifier}"

    return "https://europepmc.org/"


def search_europe_pmc(query: str, max_results: int = SEARCH_MAX_RESULTS) -> list[SearchDocument]:
    encoded_query = quote_plus(query)
    url = (
        "https://www.ebi.ac.uk/europepmc/webservices/rest/search?format=json"
        f"&pageSize={max_results}&query={encoded_query}"
    )

    with urlopen(url, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))

    results = payload.get("resultList", {}).get("result", [])
    documents = []
    for record in results:
        documents.append(
            SearchDocument(
                title=str(record.get("title", "")).strip(),
                url=build_pubmed_url(record),
                snippet=str(record.get("abstractText", "")).strip(),
                source="europe_pmc",
            )
        )
    return documents


class ExternalKnowledgeResearchTool:
    def __init__(self, max_results: int = SEARCH_MAX_RESULTS, tavily_tool=None):
        self.max_results = max_results
        self.tavily_tool = tavily_tool if tavily_tool is not None else build_tavily_tool(max_results=max_results)

    def search(self, query: str) -> list[dict[str, str]]:
        normalized_query = query.strip()
        if not normalized_query:
            return []

        if self.tavily_tool is not None:
            try:
                raw_result = self.tavily_tool.invoke(normalized_query)
                tavily_documents = normalize_tavily_results(raw_result)
                if tavily_documents:
                    return [document.__dict__ for document in tavily_documents]
            except Exception:
                pass

        try:
            documents = search_europe_pmc(normalized_query, max_results=self.max_results)
        except Exception:
            return []

        return [document.__dict__ for document in documents]

    def search_many(self, queries: list[str]) -> dict[str, list[dict[str, str]]]:
        return {query: self.search(query) for query in queries}