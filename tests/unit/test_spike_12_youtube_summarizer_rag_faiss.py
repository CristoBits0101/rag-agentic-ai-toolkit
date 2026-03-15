# --- DEPENDENCIAS ---
# 1. Sys: Para anadir la ruta del spike a los imports de prueba.
# 2. Path: Para resolver la ruta absoluta del spike.
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPIKE = ROOT / "spikes" / "12-youtube_summarizer_rag_faiss_lab"

if str(SPIKE) not in sys.path:
    sys.path.insert(0, str(SPIKE))

from config.youtube_rag_config import FAISS_QUESTION
from config.youtube_rag_config import HALLUCINATION_QUESTION
from config.youtube_rag_config import RAG_PROBLEMS_QUESTION
from config.youtube_rag_config import SAMPLE_VIDEO_URL
from orchestration.youtube_rag_orchestration import answer_question
from orchestration.youtube_rag_orchestration import build_youtube_rag_context
from orchestration.youtube_rag_orchestration import perform_similarity_search
from orchestration.youtube_rag_orchestration import summarize_video
from orchestration.youtube_transcript_orchestration import (
    build_youtube_transcript_context,
)
from orchestration.youtube_transcript_orchestration import get_transcript
from orchestration.youtube_transcript_orchestration import get_video_id
from orchestration.youtube_transcript_orchestration import process_transcript


def test_get_video_id_extracts_expected_identifier():
    assert get_video_id(SAMPLE_VIDEO_URL) == "T-D1OfcDW1M"


def test_get_transcript_returns_local_catalog_transcript():
    transcript = get_transcript(SAMPLE_VIDEO_URL)

    assert transcript
    assert len(transcript) >= 10
    assert "RAG" in transcript[0].text or "RAG" in transcript[1].text


def test_process_transcript_formats_text_and_start_times():
    transcript = get_transcript(SAMPLE_VIDEO_URL)
    processed_transcript = process_transcript(transcript)

    assert "Text:" in processed_transcript
    assert "Start:" in processed_transcript
    assert "retrieval augmented generation" in processed_transcript.lower()


def test_chunking_creates_multiple_segments():
    context = build_youtube_transcript_context(SAMPLE_VIDEO_URL)

    assert context
    assert len(context.chunks) > 1


def test_similarity_search_surfaces_faiss_chunk():
    rag_context = build_youtube_rag_context(SAMPLE_VIDEO_URL)
    documents = perform_similarity_search(rag_context.faiss_index, FAISS_QUESTION)

    assert documents
    assert any("faiss" in document.page_content.lower() for document in documents)


def test_summarize_video_mentions_rag_and_hallucinations():
    summary = summarize_video(SAMPLE_VIDEO_URL)

    assert "retrieval augmented generation" in summary.lower() or "rag" in summary.lower()
    assert "hallucination" in summary.lower()


def test_answer_question_handles_hallucinations_and_rag_problems():
    hallucination_answer = answer_question(SAMPLE_VIDEO_URL, HALLUCINATION_QUESTION)
    rag_answer = answer_question(SAMPLE_VIDEO_URL, RAG_PROBLEMS_QUESTION)

    assert "ground" in hallucination_answer.lower() or "retrieve" in hallucination_answer.lower()
    assert "knowledge cutoff" in rag_answer.lower() or "private" in rag_answer.lower()
