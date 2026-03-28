# --- DEPENDENCIAS ---
from config.story_tts_config import DEFAULT_AUDIO_FILE_NAME
from config.story_tts_config import DEFAULT_TOPIC
from config.story_tts_config import EXERCISE_TOPIC
from orchestration.story_generation_orchestration import build_story_generation_context
from orchestration.story_generation_orchestration import generate_story
from orchestration.story_real_variants_orchestration import (
    run_ollama_mistral_edge_tts_story_variant,
)


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

    audio_run = run_ollama_mistral_edge_tts_story_variant(DEFAULT_TOPIC)
    if not audio_run:
        print("Audio context could not be created.")
        return

    print(f"Topic: {story_context.topic}")
    print("\nPrompt:\n")
    print(story_context.prompt)
    print("\nGenerated Story:\n")
    print(story_context.story)
    print("\nAudio Artifact:\n")
    print(f"Provider: {audio_run.tts_provider}")
    print(f"LLM Provider: {audio_run.llm_provider}")
    print(f"LLM Model: {audio_run.llm_model}")
    print(f"Output Path: {audio_run.output_path}")
    print(f"Suggested File Name: {DEFAULT_AUDIO_FILE_NAME}")

    print_separator("EXERCISE TOPIC")
    print(f"Topic: {EXERCISE_TOPIC}")
    print("\nGenerated Story:\n")
    print(generate_story(EXERCISE_TOPIC))
