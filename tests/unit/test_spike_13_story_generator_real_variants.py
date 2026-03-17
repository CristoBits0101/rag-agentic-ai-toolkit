# --- DEPENDENCIAS ---
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPIKE = ROOT / "spikes" / "13-story_generator_text_to_speech_lab"

if str(SPIKE) not in sys.path:
    sys.path.insert(0, str(SPIKE))

from config.story_real_provider_config import MISTRAL_API_MODEL_NAME
from config.story_real_provider_config import OLLAMA_STORY_MODEL_NAME
from config.story_tts_config import DEFAULT_TOPIC
from models.story_edge_tts_gateway import synthesize_story_with_edge_tts
from models.story_mistral_api_gateway import build_mistral_request_payload
from models.story_mistral_api_gateway import extract_mistral_text
from orchestration import story_real_variants_orchestration as real_variants


def test_build_mistral_request_payload_uses_expected_model():
    payload = build_mistral_request_payload("Explain butterflies.")

    assert payload["model"] == MISTRAL_API_MODEL_NAME
    assert payload["messages"][0]["role"] == "user"
    assert "butterflies" in payload["messages"][0]["content"].lower()


def test_extract_mistral_text_returns_message_content():
    response_payload = {
        "choices": [
            {
                "message": {
                    "content": "A concise educational story.",
                }
            }
        ]
    }

    assert extract_mistral_text(response_payload) == "A concise educational story."


def test_build_real_story_variant_context_rejects_blank_topics():
    context = real_variants.build_real_story_variant_context(
        topic="   ",
        story_generator=lambda prompt: prompt,
        llm_provider="test",
        llm_model="test-model",
    )

    assert context is None


def test_run_ollama_mistral_story_variant_uses_real_wrapper_shape(monkeypatch, tmp_path):
    monkeypatch.setattr(
        real_variants,
        "generate_story_with_ollama_mistral",
        lambda prompt: "A real story about butterflies from Ollama.",
    )

    run = real_variants.run_ollama_mistral_story_variant(
        DEFAULT_TOPIC,
        output_path=tmp_path / "ollama_story.wav",
    )

    assert run
    assert run.llm_provider == "ollama"
    assert run.llm_model == OLLAMA_STORY_MODEL_NAME
    assert run.output_path.exists()
    assert run.tts_provider in {"gtts", "tone_demo"}
    assert "butterflies" in run.story.lower()


def test_run_mistral_api_story_variant_uses_real_wrapper_shape(monkeypatch, tmp_path):
    monkeypatch.setattr(
        real_variants,
        "generate_story_with_mistral_api",
        lambda prompt: "A real story about butterflies from Mistral API.",
    )

    run = real_variants.run_mistral_api_story_variant(
        DEFAULT_TOPIC,
        output_path=tmp_path / "mistral_story.wav",
    )

    assert run
    assert run.llm_provider == "mistral_api"
    assert run.llm_model == MISTRAL_API_MODEL_NAME
    assert run.output_path.exists()
    assert run.tts_provider in {"gtts", "tone_demo"}
    assert "mistral" in run.story.lower()


def test_synthesize_story_with_edge_tts_requires_cli(monkeypatch, tmp_path):
    import models.story_edge_tts_gateway as edge_tts_gateway

    class FailedRun:
        returncode = 1

    monkeypatch.setattr(
        edge_tts_gateway.subprocess,
        "run",
        lambda *args, **kwargs: FailedRun(),
    )

    try:
        synthesize_story_with_edge_tts("A story.", tmp_path / "story.mp3")
    except RuntimeError as exc:
        assert "edge-tts" in str(exc)
    else:
        raise AssertionError("The gateway should fail when edge-tts is unavailable.")


def test_run_ollama_mistral_edge_tts_story_variant_writes_audio(monkeypatch, tmp_path):
    monkeypatch.setattr(
        real_variants,
        "generate_story_with_ollama_mistral",
        lambda prompt: "A real story about butterflies with edge tts.",
    )

    def fake_edge_tts(story: str, output_path: Path) -> Path:
        path = Path(output_path)
        path.write_bytes(b"edge-tts-audio")
        return path

    original_save = real_variants.save_story_variant_with_edge_tts

    def patched_save(story_context, output_path):
        return original_save(story_context, output_path, edge_tts_generator=fake_edge_tts)

    monkeypatch.setattr(real_variants, "save_story_variant_with_edge_tts", patched_save)

    run = real_variants.run_ollama_mistral_edge_tts_story_variant(
        DEFAULT_TOPIC,
        output_path=tmp_path / "edge_story.mp3",
    )

    assert run
    assert run.llm_provider == "ollama"
    assert run.llm_model == OLLAMA_STORY_MODEL_NAME
    assert run.tts_provider == "edge_tts"
    assert run.output_path.exists()
    assert run.output_path.read_bytes() == b"edge-tts-audio"


def test_story_variant_subfolders_exist():
    assert (SPIKE / "ollama_mistral_story_tts" / "main.py").exists()
    assert (SPIKE / "mistral_api_story_tts" / "main.py").exists()
    assert (SPIKE / "ollama_mistral_edge_tts_story_tts" / "main.py").exists()
