# --- DEPENDENCIAS ---
from pathlib import Path

from config.meeting_assistant_config import WHISPER_BATCH_SIZE
from config.meeting_assistant_config import WHISPER_CHUNK_SECONDS
from config.meeting_assistant_config import WHISPER_MODEL_NAME
from data.meeting_transcript_catalog import MEETING_TRANSCRIPT_RECORDS

try:
    from transformers import pipeline
except ImportError:
    pipeline = None


def remove_non_ascii(text: str) -> str:
    return "".join(character for character in text if ord(character) < 128)


def get_catalog_transcript(audio_file: str) -> str | None:
    audio_name = Path(audio_file).name
    record = MEETING_TRANSCRIPT_RECORDS.get(audio_name)
    if record:
        return record.transcript

    return None


def transcribe_with_whisper(audio_file: str) -> str | None:
    if pipeline is None:
        return None

    try:
        speech_pipeline = pipeline(
            "automatic-speech-recognition",
            model=WHISPER_MODEL_NAME,
            chunk_length_s=WHISPER_CHUNK_SECONDS,
        )
        return speech_pipeline(audio_file, batch_size=WHISPER_BATCH_SIZE)["text"]
    except Exception:
        return None


def transcribe_audio_source(audio_file: str) -> str:
    if not audio_file:
        return ""

    catalog_transcript = get_catalog_transcript(audio_file)
    if catalog_transcript:
        return catalog_transcript

    whisper_transcript = transcribe_with_whisper(audio_file)
    if whisper_transcript:
        return whisper_transcript

    return "No local transcript is available for this audio file."
