# --- DEPENDENCIAS ---
import time
import wave
from pathlib import Path
from threading import Event

import numpy as np

from config.voice_desktop_config import AUDIO_BLOCK_SIZE
from config.voice_desktop_config import AUDIO_CHANNELS
from config.voice_desktop_config import AUDIO_SAMPLE_RATE
from config.voice_desktop_config import AUDIO_SAMPLE_WIDTH
from config.voice_desktop_config import MAX_RECORD_SECONDS
from config.voice_desktop_config import PUSH_TO_TALK_KEY
from config.voice_desktop_config import RECORDING_FILE_NAME
from config.voice_desktop_config import RUNTIME_DIR
from config.voice_desktop_config import VOICE_CHANNEL_MAX_UTTERANCE_SECONDS
from config.voice_desktop_config import VOICE_CHANNEL_MIN_SPEECH_BLOCKS
from config.voice_desktop_config import VOICE_CHANNEL_SILENCE_BLOCKS
from config.voice_desktop_config import VOICE_CHANNEL_SILENCE_THRESHOLD


def load_keyboard_module():
    try:
        import keyboard
    except ImportError as exc:
        raise RuntimeError("Install keyboard to capture push to talk input.") from exc

    return keyboard


def load_sounddevice_module():
    try:
        import sounddevice
    except ImportError as exc:
        raise RuntimeError("Install sounddevice to capture microphone audio.") from exc

    return sounddevice


def build_recording_path(
    output_dir: str | Path = RUNTIME_DIR,
    file_name: str = RECORDING_FILE_NAME,
) -> Path:
    path = Path(output_dir)
    path.mkdir(parents=True, exist_ok=True)
    return path / file_name


def write_pcm_frames_to_wav(
    frames: list[bytes],
    output_path: str | Path,
    sample_rate: int = AUDIO_SAMPLE_RATE,
    channels: int = AUDIO_CHANNELS,
    sample_width: int = AUDIO_SAMPLE_WIDTH,
) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with wave.open(str(path), "wb") as wav_file:
        wav_file.setnchannels(channels)
        wav_file.setsampwidth(sample_width)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(b"".join(frames))

    return path


class ManualAudioRecorder:
    def __init__(
        self,
        output_path: str | Path | None = None,
        sample_rate: int = AUDIO_SAMPLE_RATE,
        channels: int = AUDIO_CHANNELS,
        block_size: int = AUDIO_BLOCK_SIZE,
        sounddevice_module=None,
    ) -> None:
        self.output_path = Path(output_path) if output_path else build_recording_path()
        self.sample_rate = sample_rate
        self.channels = channels
        self.block_size = block_size
        self.sounddevice_module = sounddevice_module or load_sounddevice_module()
        self.frames: list[bytes] = []
        self.stream = None

    def _callback(self, indata, _frames, _time_info, _status) -> None:
        self.frames.append(bytes(indata))

    def start(self) -> None:
        if self.stream is not None:
            raise RuntimeError("Recording is already in progress.")

        self.frames = []
        self.stream = self.sounddevice_module.RawInputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype="int16",
            blocksize=self.block_size,
            callback=self._callback,
        )
        self.stream.start()

    def stop(self) -> Path:
        if self.stream is None:
            raise RuntimeError("Recording has not started.")

        stream = self.stream
        self.stream = None
        stream.stop()
        stream.close()

        if not self.frames:
            raise RuntimeError("No audio was captured from the microphone.")

        return write_pcm_frames_to_wav(
            self.frames,
            self.output_path,
            sample_rate=self.sample_rate,
            channels=self.channels,
        )


class ContinuousAudioChannel:
    def __init__(
        self,
        output_path: str | Path | None = None,
        sample_rate: int = AUDIO_SAMPLE_RATE,
        channels: int = AUDIO_CHANNELS,
        block_size: int = AUDIO_BLOCK_SIZE,
        silence_threshold: float = VOICE_CHANNEL_SILENCE_THRESHOLD,
        silence_blocks: int = VOICE_CHANNEL_SILENCE_BLOCKS,
        min_speech_blocks: int = VOICE_CHANNEL_MIN_SPEECH_BLOCKS,
        max_utterance_seconds: int = VOICE_CHANNEL_MAX_UTTERANCE_SECONDS,
        sounddevice_module=None,
    ) -> None:
        self.output_path = Path(output_path) if output_path else build_recording_path(file_name="voice_channel.wav")
        self.sample_rate = sample_rate
        self.channels = channels
        self.block_size = block_size
        self.silence_threshold = silence_threshold
        self.silence_blocks = silence_blocks
        self.min_speech_blocks = min_speech_blocks
        self.max_utterance_seconds = max_utterance_seconds
        self.sounddevice_module = sounddevice_module or load_sounddevice_module()
        self.stream = None
        self.stop_event = Event()

    def start(self) -> None:
        if self.stream is not None:
            raise RuntimeError("Voice channel is already open.")

        self.stop_event.clear()
        self.stream = self.sounddevice_module.RawInputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype="int16",
            blocksize=self.block_size,
        )
        self.stream.start()

    def stop(self) -> None:
        self.stop_event.set()
        if self.stream is None:
            return

        stream = self.stream
        self.stream = None
        stream.stop()
        stream.close()

    def _compute_level(self, chunk: bytes) -> float:
        samples = np.frombuffer(chunk, dtype=np.int16)
        if samples.size == 0:
            return 0.0

        return float(np.abs(samples).mean()) / 32768.0

    def capture_next_utterance(self) -> Path | None:
        if self.stream is None:
            raise RuntimeError("Voice channel has not started.")

        frames: list[bytes] = []
        speech_detected = False
        silence_run = 0
        speech_blocks = 0
        started_at = time.monotonic()

        while not self.stop_event.is_set():
            try:
                chunk, _overflowed = self.stream.read(self.block_size)
            except Exception:
                if self.stop_event.is_set() or self.stream is None:
                    return None
                raise

            chunk_bytes = bytes(chunk)
            level = self._compute_level(chunk_bytes)

            if not speech_detected:
                if level >= self.silence_threshold:
                    speech_detected = True
                    frames.append(chunk_bytes)
                    speech_blocks = 1
                    silence_run = 0
                continue

            frames.append(chunk_bytes)
            if level >= self.silence_threshold:
                speech_blocks += 1
                silence_run = 0
            else:
                silence_run += 1

            if speech_blocks >= self.min_speech_blocks and silence_run >= self.silence_blocks:
                break

            if time.monotonic() - started_at >= self.max_utterance_seconds:
                break

        if not frames:
            return None

        return write_pcm_frames_to_wav(
            frames,
            self.output_path,
            sample_rate=self.sample_rate,
            channels=self.channels,
        )


def record_audio_with_push_to_talk(
    output_path: str | Path | None = None,
    push_to_talk_key: str = PUSH_TO_TALK_KEY,
    sample_rate: int = AUDIO_SAMPLE_RATE,
    channels: int = AUDIO_CHANNELS,
    block_size: int = AUDIO_BLOCK_SIZE,
    max_record_seconds: int = MAX_RECORD_SECONDS,
    keyboard_module=None,
    sounddevice_module=None,
) -> Path:
    keyboard_module = keyboard_module or load_keyboard_module()
    sounddevice_module = sounddevice_module or load_sounddevice_module()
    path = Path(output_path) if output_path else build_recording_path()
    frames: list[bytes] = []

    with sounddevice_module.RawInputStream(
        samplerate=sample_rate,
        channels=channels,
        dtype="int16",
        blocksize=block_size,
    ) as stream:
        keyboard_module.wait(push_to_talk_key)
        start_time = time.monotonic()
        while keyboard_module.is_pressed(push_to_talk_key):
            chunk, _overflowed = stream.read(block_size)
            frames.append(bytes(chunk))
            if time.monotonic() - start_time >= max_record_seconds:
                break
            time.sleep(0.01)

    if not frames:
        raise RuntimeError("No audio was captured from the microphone.")

    return write_pcm_frames_to_wav(frames, path, sample_rate=sample_rate, channels=channels)
