# --- DEPENDENCIAS ---
import time
import wave
from pathlib import Path

from config.voice_desktop_config import AUDIO_BLOCK_SIZE
from config.voice_desktop_config import AUDIO_CHANNELS
from config.voice_desktop_config import AUDIO_SAMPLE_RATE
from config.voice_desktop_config import AUDIO_SAMPLE_WIDTH
from config.voice_desktop_config import MAX_RECORD_SECONDS
from config.voice_desktop_config import PUSH_TO_TALK_KEY
from config.voice_desktop_config import RECORDING_FILE_NAME
from config.voice_desktop_config import RUNTIME_DIR


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
