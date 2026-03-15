# --- DEPENDENCIAS ---
from config.story_tts_config import DEFAULT_AUDIO_FILE_NAME
from config.story_tts_config import DEFAULT_TOPIC
from config.story_tts_config import EXERCISE_TOPIC
from orchestration.story_audio_orchestration import build_story_audio_context
from orchestration.story_generation_orchestration import build_story_generation_context
from orchestration.story_generation_orchestration import generate_story


def print_separator(title: str) -> None:
    print("=" * 60)
    print(title)
    print("=" * 60)


def run_story_generator_text_to_speech_lab() -> None:
    print_separator("13. STORY GENERATOR AND TEXT TO SPEECH")

    story_context = build_story_generation_context(DEFAULT_TOPIC)
    if not story_context:
        print("Please provide a valid topic.")
        return

    audio_context = build_story_audio_context(DEFAULT_TOPIC)
    if not audio_context:
        print("Audio context could not be created.")
        return

    print(f"Topic: {story_context.topic}")
    print("\nPrompt:\n")
    print(story_context.prompt)
    print("\nGenerated Story:\n")
    print(story_context.story)
    print("\nAudio Artifact:\n")
    print(f"Provider: {audio_context.artifact.provider}")
    print(f"MIME Type: {audio_context.artifact.mime_type}")
    print(f"File Extension: {audio_context.artifact.file_extension}")
    print(f"Audio Bytes: {len(audio_context.artifact.audio_bytes)}")
    print(f"Suggested File Name: {DEFAULT_AUDIO_FILE_NAME}")

    print_separator("EXERCISE TOPIC")
    print(f"Topic: {EXERCISE_TOPIC}")
    print("\nGenerated Story:\n")
    print(generate_story(EXERCISE_TOPIC))
