# --- DEPENDENCIAS ---
import re
from typing import Any

from langchain_core.tools import BaseTool
from langchain_core.tools import tool
from youtube_transcript_api import YouTubeTranscriptApi
import yt_dlp

from config.youtube_tool_calling_agent_config import DEFAULT_SEARCH_LIMIT
from config.youtube_tool_calling_agent_config import DEFAULT_THUMBNAIL_LIMIT
from config.youtube_tool_calling_agent_config import MAX_TRANSCRIPT_CHARACTERS


class SilentYtDlpLogger:
    def debug(self, message: str) -> None:
        return None

    def warning(self, message: str) -> None:
        return None

    def error(self, message: str) -> None:
        return None


def build_yt_dlp_options(extract_flat: bool = False) -> dict[str, Any]:
    return {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": extract_flat,
        "skip_download": True,
        "logger": SilentYtDlpLogger(),
    }


def normalize_youtube_url(url_or_video_id: str) -> str:
    if re.match(r"^https?://", url_or_video_id):
        return url_or_video_id

    return f"https://www.youtube.com/watch?v={url_or_video_id}"


def collect_transcript_snippets(video_id: str, language: str) -> list[dict[str, Any]]:
    transcript_api = YouTubeTranscriptApi()
    transcript = transcript_api.fetch(video_id, languages=[language])
    snippets = getattr(transcript, "snippets", transcript)
    collected_snippets: list[dict[str, Any]] = []

    for snippet in snippets:
        if hasattr(snippet, "text"):
            collected_snippets.append(
                {
                    "text": snippet.text,
                    "start": getattr(snippet, "start", 0),
                    "duration": getattr(snippet, "duration", 0),
                }
            )
            continue

        if isinstance(snippet, dict):
            collected_snippets.append(
                {
                    "text": snippet.get("text", ""),
                    "start": snippet.get("start", 0),
                    "duration": snippet.get("duration", 0),
                }
            )

    return collected_snippets


@tool
def extract_video_id(url: str) -> str:
    """
    Extract the 11 character YouTube video id from a URL.

    Args:
        url: Any standard short embed or shorts YouTube URL.

    Returns:
        The extracted video id or an error message.
    """
    pattern = r"(?:v=|be/|embed/|shorts/)([a-zA-Z0-9_-]{11})"
    match = re.search(pattern, url)
    if not match:
        return "Error: Invalid YouTube URL"

    return match.group(1)


@tool
def fetch_transcript(video_id: str, language: str = "en") -> dict[str, Any]:
    """
    Fetch the transcript of a YouTube video.

    Args:
        video_id: The YouTube video id.
        language: Transcript language code.

    Returns:
        A payload with transcript text language and truncation metadata.
    """
    try:
        snippets = collect_transcript_snippets(video_id, language)
        transcript_text = " ".join(snippet["text"] for snippet in snippets).strip()
        truncated = False
        if len(transcript_text) > MAX_TRANSCRIPT_CHARACTERS:
            transcript_text = transcript_text[:MAX_TRANSCRIPT_CHARACTERS].rstrip()
            truncated = True

        return {
            "video_id": video_id,
            "language": language,
            "segment_count": len(snippets),
            "truncated": truncated,
            "transcript": transcript_text,
        }
    except Exception as exc:
        return {
            "video_id": video_id,
            "language": language,
            "error": str(exc),
        }


@tool
def search_youtube(query: str, limit: int = DEFAULT_SEARCH_LIMIT) -> list[dict[str, Any]]:
    """
    Search YouTube videos for a natural language query.

    Args:
        query: Search phrase to run against YouTube.
        limit: Maximum number of results to return.

    Returns:
        A list of video dictionaries with title id url channel and duration.
    """
    try:
        with yt_dlp.YoutubeDL(build_yt_dlp_options(extract_flat=True)) as ydl:
            results = ydl.extract_info(f"ytsearch{limit}:{query}", download=False)
        entries = results.get("entries", []) if isinstance(results, dict) else []
        collected_results: list[dict[str, Any]] = []

        for entry in entries:
            video_id = entry.get("id", "")
            collected_results.append(
                {
                    "title": entry.get("title"),
                    "video_id": video_id,
                    "url": normalize_youtube_url(video_id),
                    "channel": entry.get("channel") or entry.get("uploader"),
                    "duration": entry.get("duration"),
                }
            )

        return collected_results
    except Exception as exc:
        return [{"error": str(exc), "query": query}]


@tool
def get_full_metadata(url: str) -> dict[str, Any]:
    """
    Extract rich metadata for a YouTube video URL.

    Args:
        url: Full YouTube URL.

    Returns:
        A dictionary with title views duration channel likes comments and chapters.
    """
    try:
        with yt_dlp.YoutubeDL(build_yt_dlp_options()) as ydl:
            info = ydl.extract_info(url, download=False)

        return {
            "title": info.get("title"),
            "views": info.get("view_count"),
            "duration": info.get("duration"),
            "channel": info.get("uploader"),
            "likes": info.get("like_count"),
            "comments": info.get("comment_count"),
            "chapters": info.get("chapters", []),
            "url": info.get("webpage_url") or url,
        }
    except Exception as exc:
        return {"url": url, "error": str(exc)}


@tool
def get_thumbnails(url: str, limit: int = DEFAULT_THUMBNAIL_LIMIT) -> list[dict[str, Any]]:
    """
    Get available thumbnails for a YouTube video URL.

    Args:
        url: Full YouTube URL.
        limit: Maximum number of thumbnails to return.

    Returns:
        A list of thumbnail dictionaries with url width height and resolution.
    """
    try:
        with yt_dlp.YoutubeDL(build_yt_dlp_options()) as ydl:
            info = ydl.extract_info(url, download=False)

        thumbnails: list[dict[str, Any]] = []
        for thumbnail in info.get("thumbnails", [])[:limit]:
            if "url" not in thumbnail:
                continue
            thumbnails.append(
                {
                    "url": thumbnail["url"],
                    "width": thumbnail.get("width"),
                    "height": thumbnail.get("height"),
                    "resolution": (
                        f"{thumbnail.get('width', '')}x{thumbnail.get('height', '')}".strip("x")
                    ),
                }
            )

        return thumbnails
    except Exception as exc:
        return [{"url": url, "error": str(exc)}]


def build_youtube_agent_tools() -> list[BaseTool]:
    return [
        extract_video_id,
        fetch_transcript,
        search_youtube,
        get_full_metadata,
        get_thumbnails,
    ]


def build_tool_mapping(tools: list[BaseTool] | None = None) -> dict[str, BaseTool]:
    selected_tools = tools or build_youtube_agent_tools()
    return {tool.name: tool for tool in selected_tools}


def describe_tool_schemas(tools: list[BaseTool] | None = None) -> list[dict[str, Any]]:
    selected_tools = tools or build_youtube_agent_tools()
    return [
        {
            "name": tool.name,
            "description": tool.description,
            "args": tool.args,
        }
        for tool in selected_tools
    ]
