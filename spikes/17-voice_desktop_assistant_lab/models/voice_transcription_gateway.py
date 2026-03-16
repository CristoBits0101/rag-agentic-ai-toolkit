# --- DEPENDENCIAS ---
import wave
from pathlib import Path

import numpy as np

from config.voice_desktop_config import WHISPER_CHUNK_SECONDS
from config.voice_desktop_config import WHISPER_MODEL_NAME

try:
    from transformers import pipeline
except ImportError:
    pipeline = None


def build_whisper_pipeline(
    model_name: str = WHISPER_MODEL_NAME,
    pipeline_factory=pipeline,
):
    if pipeline_factory is None:
        raise RuntimeError("Install transformers and torch to use Whisper locally.")

    return pipeline_factory(
        "automatic-speech-recognition",
        model=model_name,
        chunk_length_s=WHISPER_CHUNK_SECONDS,
    )


def load_wav_audio_for_whisper(audio_file: str | Path) -> dict:
    path = Path(audio_file)
    if not path.exists():
        raise RuntimeError("The audio file does not exist.")

    with wave.open(str(path), "rb") as wav_file:
        sample_rate = wav_file.getframerate()
        channels = wav_file.getnchannels()
        sample_width = wav_file.getsampwidth()
        frames = wav_file.readframes(wav_file.getnframes())

    if sample_width != 2:
        raise RuntimeError("Only 16 bit PCM wav audio is supported by this practice.")

    audio_array = np.frombuffer(frames, dtype=np.int16).astype(np.float32) / 32768.0
    if channels > 1:
        audio_array = audio_array.reshape(-1, channels).mean(axis=1)

    return {
        "array": audio_array,
        "sampling_rate": sample_rate,
    }


def transcribe_audio_file(
    audio_file: str | Path,
    model_name: str = WHISPER_MODEL_NAME,
    pipeline_builder=build_whisper_pipeline,
) -> str:
    speech_pipeline = pipeline_builder(model_name=model_name)
    audio_input = load_wav_audio_for_whisper(audio_file)
    result = speech_pipeline(audio_input)
    transcript = result.get("text", "").strip() if isinstance(result, dict) else str(result).strip()
    if not transcript:
        raise RuntimeError("Whisper returned an empty transcript.")

    return transcript
