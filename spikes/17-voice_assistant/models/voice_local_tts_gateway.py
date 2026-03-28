# --- DEPENDENCIAS ---
import shutil
import subprocess
import threading

from config.voice_desktop_config import VOICE_RESPONSE_CULTURE_PREFIX
from config.voice_desktop_config import VOICE_RESPONSE_MAX_CHARS
from config.voice_desktop_config import VOICE_RESPONSE_RATE
from config.voice_desktop_config import VOICE_RESPONSE_VOLUME


def resolve_windows_speech_shell(shell_finder=shutil.which) -> str | None:
    return shell_finder("powershell.exe") or shell_finder("powershell")


def clean_text_for_speech(
    text: str,
    max_chars: int = VOICE_RESPONSE_MAX_CHARS,
) -> str:
    cleaned = " ".join((text or "").split()).strip()
    if not cleaned:
        raise RuntimeError("There is no assistant text to speak.")

    if len(cleaned) <= max_chars:
        return cleaned

    return cleaned[: max_chars - 3].rstrip() + "..."


def build_windows_speech_command(
    text: str,
    shell_path: str,
    rate: int = VOICE_RESPONSE_RATE,
    volume: int = VOICE_RESPONSE_VOLUME,
    culture_prefix: str = VOICE_RESPONSE_CULTURE_PREFIX,
) -> list[str]:
    spoken_text = clean_text_for_speech(text)
    command = (
        "Add-Type -AssemblyName System.Speech; "
        "$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
        "$voice = $synth.GetInstalledVoices() | "
        f"Where-Object {{ $_.VoiceInfo.Culture.Name -like '{culture_prefix}*' }} | "
        "Select-Object -First 1; "
        "if ($voice) { $synth.SelectVoice($voice.VoiceInfo.Name) }; "
        f"$synth.Rate = {rate}; "
        f"$synth.Volume = {volume}; "
        "$synth.Speak($args[0]);"
    )
    return [shell_path, "-NoProfile", "-Command", command, spoken_text]


def speak_text_windows_local(
    text: str,
    process_launcher=subprocess.Popen,
    shell_finder=shutil.which,
):
    shell_path = resolve_windows_speech_shell(shell_finder=shell_finder)
    if not shell_path:
        raise RuntimeError("Windows local speech is not available on this system.")

    command = build_windows_speech_command(text, shell_path=shell_path)
    return process_launcher(
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )


class LocalVoiceSpeaker:
    def __init__(
        self,
        speech_launcher=speak_text_windows_local,
        shell_finder=shutil.which,
    ) -> None:
        self.speech_launcher = speech_launcher
        self.shell_finder = shell_finder
        self.current_process = None
        self.lock = threading.Lock()

    def is_available(self) -> bool:
        return resolve_windows_speech_shell(shell_finder=self.shell_finder) is not None

    def _stop_current_process_locked(self) -> None:
        process = self.current_process
        self.current_process = None
        if process is None or process.poll() is not None:
            return

        process.terminate()
        try:
            process.wait(timeout=1)
        except Exception:
            process.kill()

    def stop(self) -> None:
        with self.lock:
            self._stop_current_process_locked()

    def speak(self, text: str):
        with self.lock:
            self._stop_current_process_locked()
            self.current_process = self.speech_launcher(
                text,
                shell_finder=self.shell_finder,
            )
            return self.current_process

    def speak_async(self, text: str) -> None:
        if not text or not text.strip():
            return

        threading.Thread(target=lambda: self.speak(text), daemon=True).start()
