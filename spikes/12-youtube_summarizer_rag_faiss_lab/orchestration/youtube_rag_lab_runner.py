# --- DEPENDENCIAS ---
from config.youtube_rag_config import FAISS_QUESTION
from config.youtube_rag_config import HALLUCINATION_QUESTION
from config.youtube_rag_config import RAG_PROBLEMS_QUESTION
from config.youtube_rag_config import SAMPLE_VIDEO_URL
from config.youtube_rag_config import SUMMARY_PREVIEW_LINES
from orchestration.youtube_rag_orchestration import answer_question
from orchestration.youtube_rag_orchestration import build_youtube_rag_context
from orchestration.youtube_rag_orchestration import perform_similarity_search
from orchestration.youtube_rag_orchestration import summarize_video
from orchestration.youtube_transcript_orchestration import (
    build_youtube_transcript_context,
)
from orchestration.youtube_transcript_orchestration import get_video_id

# --- RUNNER ---
def print_section(title: str):
    # Separa visualmente cada seccion del laboratorio.
    print(f"\n=== {title} ===")


def print_documents(documents):
    # Imprime los chunks recuperados para una consulta.
    for index, document in enumerate(documents, start=1):
        snippet = " ".join(document.page_content.split())[:180]
        print(f"{index}. {snippet}")


def run_youtube_summarizer_rag_faiss_lab():
    # Ejecuta la practica completa de resumen y QA sobre un video catalogado.
    transcript_context = build_youtube_transcript_context(SAMPLE_VIDEO_URL)
    rag_context = build_youtube_rag_context(SAMPLE_VIDEO_URL)

    print("Practica 12 AI Powered YouTube Summarizer QA Tool With RAG LangChain And FAISS")

    print_section("Video Setup")
    print(f"URL: {SAMPLE_VIDEO_URL}")
    print(f"Video ID: {get_video_id(SAMPLE_VIDEO_URL)}")
    print(f"Transcript segments: {len(transcript_context.transcript) if transcript_context else 0}")

    print_section("Processed Transcript Preview")
    if transcript_context:
        preview_lines = transcript_context.processed_transcript.splitlines()[
            :SUMMARY_PREVIEW_LINES
        ]
        for line in preview_lines:
            print(line)

    print_section("Chunking And FAISS")
    print(f"Chunks created: {len(rag_context.chunks) if rag_context else 0}")
    if rag_context:
        print(f"FAISS indexed chunks: {rag_context.faiss_index.index.ntotal}")

    print_section("Summary")
    print(summarize_video(SAMPLE_VIDEO_URL))

    print_section("Similarity Search")
    if rag_context:
        print(f"Query: {FAISS_QUESTION}")
        print_documents(perform_similarity_search(rag_context.faiss_index, FAISS_QUESTION))

    print_section("Question Answering")
    print(f"Question: {HALLUCINATION_QUESTION}")
    print(answer_question(SAMPLE_VIDEO_URL, HALLUCINATION_QUESTION))
    print(f"\nQuestion: {RAG_PROBLEMS_QUESTION}")
    print(answer_question(SAMPLE_VIDEO_URL, RAG_PROBLEMS_QUESTION))
