# --- DEPENDENCIAS ---
import io
import math
import re
import struct
import wave
from dataclasses import dataclass
from pathlib import Path

from config.story_tts_config import AUDIO_AMPLITUDE
from config.story_tts_config import AUDIO_GAP_SECONDS
from config.story_tts_config import AUDIO_SAMPLE_RATE
from config.story_tts_config import AUDIO_TONE_SECONDS
from config.story_tts_config import ONLINE_TTS_ENABLED

try:
    from gtts import gTTS
except ImportError:
    gTTS = None

# --- AUDIO ---
@dataclass(frozen=True)
class StoryAudioArtifact:
    audio_bytes: bytes
    mime_type: str
    file_extension: str
    provider: str


def split_story_units(story: str) -> list[str]:
    units = [unit.strip() for unit in re.split(r"[.!?]+", story) if unit.strip()]
    return units or [story.strip() or "story"]


def build_unit_frequencies(story: str) -> list[int]:
    frequencies = []

    for index, unit in enumerate(split_story_units(story)):
        base = 260 + ((len(unit.split()) + index) % 6) * 40
        frequencies.append(base)

    return frequencies[:16] or [300]


def build_demo_wav_bytes(story: str) -> bytes:
    buffer = io.BytesIO()

    with wave.open(buffer, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(AUDIO_SAMPLE_RATE)

        tone_frames = int(AUDIO_SAMPLE_RATE * AUDIO_TONE_SECONDS)
        gap_frames = int(AUDIO_SAMPLE_RATE * AUDIO_GAP_SECONDS)

        for frequency in build_unit_frequencies(story):
            for frame in range(tone_frames):
                phase = 2 * math.pi * frequency * frame / AUDIO_SAMPLE_RATE
                sample = int(AUDIO_AMPLITUDE * math.sin(phase))
                wav_file.writeframesraw(struct.pack("<h", sample))

            if gap_frames:
                wav_file.writeframesraw(b"\x00\x00" * gap_frames)

    return buffer.getvalue()


def build_online_tts_audio(story: str) -> StoryAudioArtifact | None:
    if not gTTS:
        return None

    try:
        buffer = io.BytesIO()
        gTTS(story).write_to_fp(buffer)
        return StoryAudioArtifact(
            audio_bytes=buffer.getvalue(),
            mime_type="audio/mpeg",
            file_extension="mp3",
            provider="gtts",
        )
    except Exception:
        return None


def synthesize_story_audio(
    story: str,
    prefer_online_tts: bool = ONLINE_TTS_ENABLED,
) -> StoryAudioArtifact:
    if prefer_online_tts:
        online_artifact = build_online_tts_audio(story)
        if online_artifact:
            return online_artifact

    return StoryAudioArtifact(
        audio_bytes=build_demo_wav_bytes(story),
        mime_type="audio/wav",
        file_extension="wav",
        provider="tone_demo",
    )


def save_audio_artifact(artifact: StoryAudioArtifact, output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(artifact.audio_bytes)
    return path
