# --- DEPENDENCIAS ---
# 1. Sys: Para anadir la ruta del spike a los imports de prueba.
# 2. Path: Para resolver la ruta absoluta del spike.
import sys
from pathlib import Path

from langchain_core.runnables import RunnableLambda

ROOT = Path(__file__).resolve().parents[2]
SPIKE = ROOT / "spikes" / "15-meeting_assistant"

if str(SPIKE) not in sys.path:
    sys.path.insert(0, str(SPIKE))

from config.meeting_assistant_config import SAMPLE_AUDIO_FILE_NAME
from orchestration.meeting_assistant_orchestration import transcript_audio
from orchestration.meeting_cleanup_orchestration import extract_adjusted_transcript
from orchestration.meeting_cleanup_orchestration import product_assistant
from orchestration.meeting_minutes_orchestration import create_meeting_minutes_prompt
from orchestration.meeting_minutes_orchestration import generate_meeting_minutes
from orchestration.meeting_transcription_orchestration import remove_non_ascii
from orchestration.meeting_transcription_orchestration import transcribe_audio_source
from ui.meeting_assistant_ui import build_interface


def test_remove_non_ascii_strips_extended_characters():
    result = remove_non_ascii("Reunion con cafe y emoji ðŸ˜€")

    assert result == "Reunion con cafe y emoji "


def test_transcribe_audio_source_returns_catalog_transcript():
    transcript = transcribe_audio_source(SAMPLE_AUDIO_FILE_NAME)

    assert "401k migration" in transcript
    assert "HSA FAQ" in transcript


def test_product_assistant_formats_financial_terms():
    from orchestration import meeting_cleanup_orchestration as cleanup_orchestration

    original_builder = cleanup_orchestration.build_meeting_assistant_llm
    cleanup_orchestration.build_meeting_assistant_llm = lambda: RunnableLambda(
        lambda prompt: (
            "Adjusted Transcript:\n"
            "We discussed the 401(k) retirement savings plan migration and the Health Savings Account (HSA) FAQ "
            "while lowering Loan to Value (LTV) to 80 percent.\n"
            "Changed Terms:\n401k -> 401(k) retirement savings plan\n"
        )
    )
    cleanup_response = product_assistant(
        "We discussed the 401k migration and the hsa faq while lowering ltv to eighty percent."
    )
    cleanup_orchestration.build_meeting_assistant_llm = original_builder
    adjusted_transcript = extract_adjusted_transcript(cleanup_response)

    assert "401(k) retirement savings plan" in adjusted_transcript
    assert "Health Savings Account (HSA)" in adjusted_transcript
    assert "Loan to Value (LTV)" in adjusted_transcript
    assert "80 percent" in adjusted_transcript


def test_prompt_template_mentions_meeting_minutes_and_tasks():
    prompt = create_meeting_minutes_prompt().format(context="demo context")

    assert "Meeting Minutes:" in prompt
    assert "Task List:" in prompt
    assert "demo context" in prompt


def test_generate_meeting_minutes_returns_structured_output():
    from orchestration import meeting_minutes_orchestration as minutes_orchestration

    original_builder = minutes_orchestration.build_meeting_assistant_llm
    minutes_orchestration.build_meeting_assistant_llm = lambda: RunnableLambda(
        lambda prompt: (
            "Meeting Minutes:\n"
            "- The team reviewed the 401(k) retirement savings plan rollout.\n"
            "Task List:\n"
            "- Maria: Update the FAQ and share it next week.\n"
        )
    )
    result = generate_meeting_minutes(
        "The team reviewed the 401(k) retirement savings plan rollout and Maria owns the FAQ update."
    )
    minutes_orchestration.build_meeting_assistant_llm = original_builder

    assert "Meeting Minutes:" in result
    assert "Task List:" in result
    assert "Maria:" in result


def test_transcript_audio_writes_downloadable_report(tmp_path, monkeypatch):
    output_path = tmp_path / "meeting_minutes_and_tasks.txt"
    monkeypatch.setattr(
        "orchestration.meeting_assistant_orchestration.OUTPUT_FILE_NAME",
        str(output_path),
    )
    from orchestration import meeting_cleanup_orchestration as cleanup_orchestration
    from orchestration import meeting_minutes_orchestration as minutes_orchestration

    original_cleanup_builder = cleanup_orchestration.build_meeting_assistant_llm
    original_minutes_builder = minutes_orchestration.build_meeting_assistant_llm
    cleanup_orchestration.build_meeting_assistant_llm = lambda: RunnableLambda(
        lambda prompt: (
            "Adjusted Transcript:\n"
            "The 401(k) retirement savings plan migration is on track and the Health Savings Account (HSA) FAQ needs edits.\n"
            "Changed Terms:\n401k -> 401(k) retirement savings plan\n"
        )
    )
    minutes_orchestration.build_meeting_assistant_llm = lambda: RunnableLambda(
        lambda prompt: (
            "Meeting Minutes:\n"
            "- The rollout remains on track.\n"
            "Task List:\n"
            "- Maria: Publish the updated FAQ.\n"
        )
    )

    result, saved_file = transcript_audio(SAMPLE_AUDIO_FILE_NAME)
    cleanup_orchestration.build_meeting_assistant_llm = original_cleanup_builder
    minutes_orchestration.build_meeting_assistant_llm = original_minutes_builder

    assert "Meeting Minutes:" in result
    assert "Task List:" in result
    assert Path(saved_file).exists()
    assert Path(saved_file).read_text(encoding="utf-8").startswith("Meeting Minutes:")


def test_build_interface_returns_gradio_interface():
    interface = build_interface()

    assert hasattr(interface, "launch")
    assert interface.title == "AI Meeting Assistant"
