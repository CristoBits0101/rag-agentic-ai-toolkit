# --- DEPENDENCIAS ---
from config.meeting_assistant_config import SAMPLE_AUDIO_FILE_NAME
from orchestration.meeting_assistant_orchestration import transcript_audio


def print_separator(title: str) -> None:
    print("=" * 60)
    print(title)
    print("=" * 60)


def run_ai_meeting_assistant_lab() -> None:
    print_separator("15. AI MEETING ASSISTANT")
    result, output_file = transcript_audio(SAMPLE_AUDIO_FILE_NAME)
    print(result)
    print()
    print(f"Output file: {output_file}")
