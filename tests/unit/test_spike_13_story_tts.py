# --- DEPENDENCIAS ---
# 1. Sys: Para anadir la ruta del spike a los imports de prueba.
# 2. Path: Para resolver la ruta absoluta del spike.
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPIKE = ROOT / "spikes" / "13-story_tts"

if str(SPIKE) not in sys.path:
    sys.path.insert(0, str(SPIKE))

from config.story_tts_config import DEFAULT_TOPIC
from config.story_tts_config import EXERCISE_TOPIC
from orchestration.story_audio_orchestration import build_story_audio_context
from orchestration.story_audio_orchestration import save_generated_story_audio
from orchestration.story_generation_orchestration import create_story_prompt
from orchestration.story_generation_orchestration import generate_story


def build_fake_story_from_prompt(prompt: str) -> str:
    lowered_prompt = prompt.lower()
    if "butterflies" in lowered_prompt:
        return (
            "A butterfly begins as an egg then becomes a caterpillar enters a chrysalis "
            "and finally emerges as an adult butterfly. Summary: butterflies grow through clear stages."
        )

    return (
        "A human starts life as a baby moves through childhood and eventually reaches adulthood. "
        "Summary: people develop through several life stages."
    )


def test_create_story_prompt_mentions_topic_and_word_range():
    prompt = create_story_prompt(DEFAULT_TOPIC)

    assert DEFAULT_TOPIC in prompt
    assert "200-300 words" in prompt


def test_generate_story_for_butterflies_mentions_key_stages():
    from orchestration import story_generation_orchestration as generation_orchestration

    generation_orchestration.build_story_generation_context.cache_clear()
    original_generator = generation_orchestration.generate_story_with_ollama_mistral
    generation_orchestration.generate_story_with_ollama_mistral = build_fake_story_from_prompt
    story = generate_story(DEFAULT_TOPIC)
    lowered_story = story.lower()
    generation_orchestration.generate_story_with_ollama_mistral = original_generator
    generation_orchestration.build_story_generation_context.cache_clear()

    assert "butterflies" in lowered_story or "butterfly" in lowered_story
    assert "caterpillar" in lowered_story
    assert "chrysalis" in lowered_story
    assert "summary" in lowered_story


def test_generate_story_for_human_life_cycle_mentions_growth_stages():
    from orchestration import story_generation_orchestration as generation_orchestration

    generation_orchestration.build_story_generation_context.cache_clear()
    original_generator = generation_orchestration.generate_story_with_ollama_mistral
    generation_orchestration.generate_story_with_ollama_mistral = build_fake_story_from_prompt
    story = generate_story(EXERCISE_TOPIC)
    lowered_story = story.lower()
    generation_orchestration.generate_story_with_ollama_mistral = original_generator
    generation_orchestration.build_story_generation_context.cache_clear()

    assert "infant" in lowered_story or "baby" in lowered_story
    assert "childhood" in lowered_story
    assert "adulthood" in lowered_story or "adult" in lowered_story


def test_generate_story_rejects_blank_topics():
    assert generate_story("   ") == "Please provide a valid topic."


def test_build_story_audio_context_returns_local_audio_artifact():
    from orchestration import story_generation_orchestration as generation_orchestration

    generation_orchestration.build_story_generation_context.cache_clear()
    original_generator = generation_orchestration.generate_story_with_ollama_mistral
    generation_orchestration.generate_story_with_ollama_mistral = build_fake_story_from_prompt
    audio_context = build_story_audio_context(DEFAULT_TOPIC)
    generation_orchestration.generate_story_with_ollama_mistral = original_generator
    generation_orchestration.build_story_generation_context.cache_clear()

    assert audio_context
    assert "butterfly" in audio_context.story.lower()
    assert audio_context.artifact.provider == "tone_demo"
    assert audio_context.artifact.mime_type == "audio/wav"
    assert len(audio_context.artifact.audio_bytes) > 44


def test_save_generated_story_audio_writes_wav_file(tmp_path):
    from orchestration import story_generation_orchestration as generation_orchestration

    generation_orchestration.build_story_generation_context.cache_clear()
    original_generator = generation_orchestration.generate_story_with_ollama_mistral
    generation_orchestration.generate_story_with_ollama_mistral = build_fake_story_from_prompt
    output_path = tmp_path / "generated_story.wav"
    saved_path = save_generated_story_audio(DEFAULT_TOPIC, output_path)
    generation_orchestration.generate_story_with_ollama_mistral = original_generator
    generation_orchestration.build_story_generation_context.cache_clear()

    assert saved_path == output_path
    assert output_path.exists()
    assert output_path.read_bytes()[:4] == b"RIFF"
