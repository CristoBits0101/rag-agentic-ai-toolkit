# --- DEPENDENCIAS ---
import sys
from pathlib import Path
from typing import Any

from langchain_core.messages import AIMessage
from langchain_core.tools import tool

ROOT = Path(__file__).resolve().parents[2]
SPIKE = ROOT / "spikes" / "21-youtube_tool_calling_agent_lab"

if str(SPIKE) not in sys.path:
    sys.path.insert(0, str(SPIKE))

from models.youtube_tool_calling_ollama_gateway import select_best_available_ollama_model
from orchestration.youtube_tool_calling_agent_orchestration import (
    YouTubeToolCallingAgent,
)
from orchestration.youtube_tool_calling_agent_orchestration import (
    build_fixed_summarization_chain,
)
from orchestration.youtube_tool_calling_agent_orchestration import (
    execute_manual_youtube_summary_flow,
)
from orchestration.youtube_tool_calling_agent_orchestration import (
    execute_tool,
)
from orchestration.youtube_tool_calling_agent_orchestration import (
    extract_final_response_content,
)
from orchestration.youtube_tool_calling_tools_orchestration import describe_tool_schemas
from orchestration.youtube_tool_calling_tools_orchestration import extract_video_id


@tool
def fake_extract_video_id(url: str) -> str:
    """
    Extract the video id from a URL for tests.

    Args:
        url: Video URL.

    Returns:
        Fixed video id.
    """
    return "T-D1OfcDW1M"


fake_extract_video_id.name = "extract_video_id"


@tool
def fake_fetch_transcript(video_id: str, language: str = "en") -> dict[str, Any]:
    """
    Fetch a fake transcript for tests.

    Args:
        video_id: Video identifier.
        language: Transcript language.

    Returns:
        Fake transcript payload.
    """
    return {
        "video_id": video_id,
        "language": language,
        "segment_count": 2,
        "truncated": False,
        "transcript": "This is a short transcript about retrieval augmented generation.",
    }


fake_fetch_transcript.name = "fetch_transcript"


@tool
def fake_search_youtube(query: str, limit: int = 5) -> list[dict[str, Any]]:
    """
    Search fake YouTube results for tests.

    Args:
        query: Search phrase.
        limit: Maximum results.

    Returns:
        Search result list.
    """
    return [
        {
            "title": "LangChain Tool Calling Demo",
            "video_id": "abc12345678",
            "url": "https://www.youtube.com/watch?v=abc12345678",
            "channel": "Demo Channel",
            "duration": 600,
        }
    ]


fake_search_youtube.name = "search_youtube"


@tool
def fake_get_full_metadata(url: str) -> dict[str, Any]:
    """
    Return fake metadata for tests.

    Args:
        url: Video URL.

    Returns:
        Metadata payload.
    """
    return {
        "title": "LangChain Tool Calling Demo",
        "views": 1000,
        "duration": 600,
        "channel": "Demo Channel",
        "likes": 100,
        "comments": 10,
        "chapters": [],
        "url": url,
    }


fake_get_full_metadata.name = "get_full_metadata"


@tool
def fake_get_thumbnails(url: str, limit: int = 5) -> list[dict[str, Any]]:
    """
    Return fake thumbnails for tests.

    Args:
        url: Video URL.
        limit: Maximum thumbnails.

    Returns:
        Thumbnail list.
    """
    return [
        {
            "url": "https://img.youtube.com/vi/abc12345678/hqdefault.jpg",
            "width": 480,
            "height": 360,
            "resolution": "480x360",
        }
    ]


fake_get_thumbnails.name = "get_thumbnails"


class ManualSummaryModel:
    def __init__(self):
        self._call_count = 0

    def bind_tools(self, tools):
        return self

    def invoke(self, messages):
        self._call_count += 1

        if self._call_count == 1:
            return AIMessage(
                content="",
                tool_calls=[
                    {
                        "name": "extract_video_id",
                        "args": {"url": "https://www.youtube.com/watch?v=T-D1OfcDW1M"},
                        "id": "call_extract",
                        "type": "tool_call",
                    }
                ],
            )

        if self._call_count == 2:
            return AIMessage(
                content="",
                tool_calls=[
                    {
                        "name": "fetch_transcript",
                        "args": {"video_id": "T-D1OfcDW1M", "language": "en"},
                        "id": "call_transcript",
                        "type": "tool_call",
                    }
                ],
            )

        return AIMessage(content="The video explains retrieval augmented generation in clear terms.")


class RecursiveSearchModel:
    def __init__(self):
        self._call_count = 0

    def bind_tools(self, tools):
        return self

    def invoke(self, messages):
        self._call_count += 1

        if self._call_count == 1:
            return AIMessage(
                content="",
                tool_calls=[
                    {
                        "name": "search_youtube",
                        "args": {"query": "LangChain tool calling", "limit": 1},
                        "id": "call_search",
                        "type": "tool_call",
                    }
                ],
            )

        if self._call_count == 2:
            return AIMessage(
                content="",
                tool_calls=[
                    {
                        "name": "get_full_metadata",
                        "args": {"url": "https://www.youtube.com/watch?v=abc12345678"},
                        "id": "call_metadata",
                        "type": "tool_call",
                    },
                    {
                        "name": "get_thumbnails",
                        "args": {"url": "https://www.youtube.com/watch?v=abc12345678", "limit": 1},
                        "id": "call_thumbnails",
                        "type": "tool_call",
                    },
                ],
            )

        return AIMessage(content="The first result is LangChain Tool Calling Demo by Demo Channel.")


def build_fake_manual_tools():
    return [fake_extract_video_id, fake_fetch_transcript]


def build_fake_recursive_tools():
    return [fake_search_youtube, fake_get_full_metadata, fake_get_thumbnails]


def test_extract_video_id_handles_valid_and_invalid_urls():
    assert extract_video_id.invoke(
        {"url": "https://www.youtube.com/watch?v=T-D1OfcDW1M"}
    ) == "T-D1OfcDW1M"
    assert extract_video_id.invoke({"url": "https://example.com/video"}) == "Error: Invalid YouTube URL"


def test_describe_tool_schemas_lists_expected_arguments():
    schemas = describe_tool_schemas()
    schema_by_name = {schema["name"]: schema for schema in schemas}

    assert "url" in schema_by_name["extract_video_id"]["args"]
    assert "video_id" in schema_by_name["fetch_transcript"]["args"]
    assert "query" in schema_by_name["search_youtube"]["args"]


def test_execute_tool_serializes_dictionary_results():
    tool_mapping = {"fetch_transcript": fake_fetch_transcript}
    tool_message = execute_tool(
        {
            "name": "fetch_transcript",
            "args": {"video_id": "T-D1OfcDW1M", "language": "en"},
            "id": "call_transcript",
            "type": "tool_call",
        },
        tool_mapping,
    )

    assert '"video_id": "T-D1OfcDW1M"' in str(tool_message.content)
    assert tool_message.tool_call_id == "call_transcript"


def test_execute_manual_youtube_summary_flow_runs_two_tool_steps():
    result = execute_manual_youtube_summary_flow(
        query="Summarize this YouTube video in english.",
        tools=build_fake_manual_tools(),
        model=ManualSummaryModel(),
    )

    assert [tool_call.tool_name for tool_call in result.tool_calls] == [
        "extract_video_id",
        "fetch_transcript",
    ]
    assert [step.tool_name for step in result.steps] == [
        "extract_video_id",
        "fetch_transcript",
    ]
    assert "retrieval augmented generation" in result.final_answer.lower()


def test_fixed_summarization_chain_returns_summary_text():
    chain = build_fixed_summarization_chain(
        model=ManualSummaryModel(),
        tools=build_fake_manual_tools(),
    )

    result = chain.invoke({"query": "Summarize this YouTube video in english."})

    assert "retrieval augmented generation" in result.lower()


def test_recursive_agent_handles_search_metadata_and_thumbnails():
    agent = YouTubeToolCallingAgent(
        model=RecursiveSearchModel(),
        tools=build_fake_recursive_tools(),
    )

    result = agent.run("Search YouTube for LangChain tool calling and return metadata and thumbnails.")

    assert "LangChain Tool Calling Demo" in result


def test_extract_final_response_content_falls_back_to_previous_message_content():
    messages = [
        AIMessage(content=""),
        AIMessage(content="Final answer from previous step."),
        AIMessage(content=""),
    ]

    assert extract_final_response_content(messages) == "Final answer from previous step."


def test_select_best_available_ollama_model_prefers_ranked_candidate():
    selected_model = select_best_available_ollama_model(
        ["llama3.2:3b", "qwen2.5:7b", "mistral"],
    )

    assert selected_model == "qwen2.5:7b"
