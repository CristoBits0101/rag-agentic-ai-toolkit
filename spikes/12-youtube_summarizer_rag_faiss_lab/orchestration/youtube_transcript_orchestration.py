# --- DEPENDENCIAS ---
# 1. Dataclass: Para transportar el estado de un video ya procesado.
# 2. Functools: Para cachear el pipeline por video.
# 3. Regex: Para extraer el identificador del video.
from dataclasses import dataclass
from functools import lru_cache
import re

from langchain.text_splitter import RecursiveCharacterTextSplitter

from config.youtube_rag_config import CHUNK_OVERLAP
from config.youtube_rag_config import CHUNK_SIZE
from data.youtube_transcript_catalog import TranscriptSegment
from data.youtube_transcript_catalog import YOUTUBE_TRANSCRIPT_CATALOG

# --- TRANSCRIPTO ---
@dataclass(frozen=True)
class YouTubeTranscriptContext:
    video_id: str
    transcript: list[TranscriptSegment]
    processed_transcript: str
    chunks: list[str]


def get_video_id(url: str) -> str | None:
    # Extrae el identificador de video desde URLs de YouTube comunes.
    patterns = [
        r"https:\/\/www\.youtube\.com\/watch\?v=([a-zA-Z0-9_-]{11})",
        r"https:\/\/youtu\.be\/([a-zA-Z0-9_-]{11})",
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    return None


def get_transcript(url: str) -> list[TranscriptSegment] | None:
    # Recupera el transcript local asociado al video.
    video_id = get_video_id(url)
    if not video_id:
        return None

    return YOUTUBE_TRANSCRIPT_CATALOG.get(video_id)


def process_transcript(transcript: list[TranscriptSegment]) -> str:
    # Convierte el transcript estructurado en una cadena lineal.
    lines = [f"Text: {segment.text} Start: {segment.start}" for segment in transcript]
    return "\n".join(lines)


def chunk_transcript(
    processed_transcript: str,
    chunk_size: int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP,
) -> list[str]:
    # Divide el transcript para retrieval con solape de contexto.
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    return splitter.split_text(processed_transcript)


@lru_cache(maxsize=8)
def build_youtube_transcript_context(video_url: str) -> YouTubeTranscriptContext | None:
    # Ejecuta el pipeline de transcript procesado y chunking.
    transcript = get_transcript(video_url)
    if not transcript:
        return None

    video_id = get_video_id(video_url)
    processed_transcript = process_transcript(transcript)
    chunks = chunk_transcript(processed_transcript)
    return YouTubeTranscriptContext(
        video_id=video_id or "",
        transcript=transcript,
        processed_transcript=processed_transcript,
        chunks=chunks,
    )
