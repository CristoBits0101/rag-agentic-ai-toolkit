# --- DEPENDENCIAS ---

OLLAMA_TAGS_URL = "http://127.0.0.1:11434/api/tags"
OLLAMA_MODEL_CANDIDATES = (
    "qwen2.5:7b",
    "llama3.2:3b",
    "mistral",
)

LAB_INTRODUCTION = (
    "Practica 21 adapta el lab de Build a Tool Calling Agent con ChatOllama "
    "y herramientas reales sobre YouTube usando yt-dlp y youtube-transcript-api."
)

YOUTUBE_TOOL_SYSTEM_PROMPT = (
    "You are a YouTube tool calling agent. "
    "Use tools whenever a request needs YouTube search video id extraction transcripts metadata or thumbnails. "
    "For video summaries from a URL first extract the video id then fetch the transcript then summarize it. "
    "For discovery requests search YouTube first and then call metadata or thumbnail tools for the selected videos. "
    "Do not invent video details when a tool can provide them."
)

YOUTUBE_TOOL_RETRY_PROMPT = (
    "Retry the last request and answer by calling the appropriate YouTube tools with structured arguments."
)

SAMPLE_VIDEO_URL = "https://www.youtube.com/watch?v=T-D1OfcDW1M"
DIRECT_SEARCH_QUERY = "LangChain tool calling"
MANUAL_SUMMARY_QUERY = (
    "I want to summarize youtube video: https://www.youtube.com/watch?v=T-D1OfcDW1M in english"
)
FIXED_CHAIN_QUERY = MANUAL_SUMMARY_QUERY
UNIVERSAL_CHAIN_QUERY = (
    "Search YouTube for LangChain tool calling and return metadata and thumbnails for the first result."
)

DEFAULT_SEARCH_LIMIT = 5
DEFAULT_THUMBNAIL_LIMIT = 5
MAX_TRANSCRIPT_CHARACTERS = 16000
MAX_RECURSIVE_TOOL_ITERATIONS = 6
