# --- DEPENDENCIAS ---
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
SPIKE_ROOT = PROJECT_ROOT / "spikes" / "17-voice_assistant"
RUNTIME_DIR = SPIKE_ROOT / "runtime"
RECORDING_FILE_NAME = "voice_command.wav"
UI_WINDOW_TITLE = "Voice Desktop Assistant"
UI_WINDOW_SIZE = "920x640"
OLLAMA_API_URL = "http://127.0.0.1:11434/api/chat"
OLLAMA_TAGS_URL = "http://127.0.0.1:11434/api/tags"
VOICE_RESPONSE_ENABLED_BY_DEFAULT = True
VOICE_RESPONSE_MAX_CHARS = 320
VOICE_RESPONSE_RATE = 0
VOICE_RESPONSE_VOLUME = 100
VOICE_RESPONSE_CULTURE_PREFIX = "es-"
OLLAMA_MODEL_CANDIDATES = (
    "qwen3-vl:30b",
    "qwen3-vl:8b",
    "qwen2.5:7b",
    "qwen2.5:7b-instruct",
    "llama3.1:8b",
    "llama3.2:3b",
    "mistral",
)
OLLAMA_SCREEN_VISION_MODEL_CANDIDATES = (
    "qwen3-vl:30b",
    "qwen3-vl:8b",
)
USE_OLLAMA_BY_DEFAULT = True
WHISPER_MODEL_NAME = "openai/whisper-small"
WHISPER_LANGUAGE = "spanish"
WHISPER_TASK = "transcribe"
WHISPER_CHUNK_SECONDS = 15
AUDIO_SAMPLE_RATE = 16000
AUDIO_CHANNELS = 1
AUDIO_SAMPLE_WIDTH = 2
AUDIO_BLOCK_SIZE = 2048
MAX_RECORD_SECONDS = 20
PUSH_TO_TALK_KEY = "space"
VOICE_CHANNEL_MAX_UTTERANCE_SECONDS = 12
VOICE_CHANNEL_SILENCE_THRESHOLD = 0.015
VOICE_CHANNEL_SILENCE_BLOCKS = 10
VOICE_CHANNEL_MIN_SPEECH_BLOCKS = 3
CONFIRMATION_KEYWORDS = {"confirmar", "si", "adelante", "ejecuta", "aceptar", "ok"}
CANCELLATION_KEYWORDS = {"cancelar", "no", "detener", "anular", "parar"}
EXIT_KEYWORDS = {"salir", "cerrar asistente", "terminar", "adios"}
SENSITIVE_ACTIONS = {"close_application", "trash_path"}
PROTECTED_PATH_FRAGMENTS = (
    "\\windows\\",
    "\\program files\\",
    "\\program files (x86)\\",
    "\\system32\\",
)
DEFAULT_CONFIRMATION_PROMPT = "Accion sensible detectada. Di confirmar o cancelar."
CLICK_MATCH_CONFIDENCE = 0.9
SCREEN_VISION_MIN_CONFIDENCE = 0.6
APPLICATION_STARTUP_DELAY_SECONDS = 3.0
CLICK_TARGET_RETRY_ATTEMPTS = 6
CLICK_TARGET_RETRY_DELAY_SECONDS = 2.0
