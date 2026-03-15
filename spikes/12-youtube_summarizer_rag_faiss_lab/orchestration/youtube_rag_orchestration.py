# --- DEPENDENCIAS ---
from dataclasses import dataclass
from functools import lru_cache

from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS

from config.youtube_rag_config import RETRIEVAL_TOP_K
from models.youtube_rag_demo_llm import build_youtube_rag_demo_llm
from models.youtube_rag_embedding_gateway import build_youtube_rag_embeddings
from orchestration.youtube_transcript_orchestration import (
    build_youtube_transcript_context,
)

# --- RAG ---
@dataclass(frozen=True)
class YouTubeRagContext:
    processed_transcript: str
    chunks: list[str]
    faiss_index: FAISS


def create_faiss_index(chunks: list[str]) -> FAISS:
    # Construye un vector store FAISS desde los chunks del transcript.
    return FAISS.from_texts(chunks, build_youtube_rag_embeddings())


def perform_similarity_search(
    faiss_index: FAISS,
    query: str,
    k: int = RETRIEVAL_TOP_K,
):
    # Recupera los chunks mas cercanos para una consulta.
    return faiss_index.similarity_search(query, k=k)


def retrieve(query: str, faiss_index: FAISS, k: int = RETRIEVAL_TOP_K):
    # Reutiliza la busqueda vectorial para el flujo QA.
    return perform_similarity_search(faiss_index, query, k=k)


def format_documents_for_prompt(documents) -> str:
    # Une el contexto recuperado en un solo bloque de texto.
    return "\n\n".join(document.page_content for document in documents)


def create_summary_prompt() -> PromptTemplate:
    # Crea el prompt de resumen del transcript.
    template = """
You are an AI assistant tasked with summarizing YouTube video transcripts.

Instructions:
1. Summarize the transcript in a single concise paragraph.
2. Ignore timestamps in the summary.
3. Focus on the spoken content.

Please summarize the following YouTube video transcript:

{transcript}
"""
    return PromptTemplate.from_template(template)


def create_qa_prompt_template() -> PromptTemplate:
    # Crea el prompt para responder sobre el video usando contexto recuperado.
    template = """
You are an expert assistant providing detailed and accurate answers based on the following video content.

Relevant Video Context: {context}

Based on the above context please answer the following question.
Question: {question}
"""
    return PromptTemplate.from_template(template)


def create_summary_chain():
    # Construye una cadena moderna de resumen con prompt y LLM.
    return create_summary_prompt() | build_youtube_rag_demo_llm()


def create_qa_chain():
    # Construye una cadena moderna de QA con prompt y LLM.
    return create_qa_prompt_template() | build_youtube_rag_demo_llm()


@lru_cache(maxsize=8)
def build_youtube_rag_context(video_url: str) -> YouTubeRagContext | None:
    # Construye y cachea el indice FAISS de un transcript procesado.
    transcript_context = build_youtube_transcript_context(video_url)
    if not transcript_context:
        return None

    faiss_index = create_faiss_index(transcript_context.chunks)
    return YouTubeRagContext(
        processed_transcript=transcript_context.processed_transcript,
        chunks=transcript_context.chunks,
        faiss_index=faiss_index,
    )


def summarize_video(video_url: str) -> str:
    # Resume el transcript del video solicitado.
    rag_context = build_youtube_rag_context(video_url)
    if not rag_context:
        return "Please provide a valid YouTube URL with a supported local transcript."

    summary_chain = create_summary_chain()
    return summary_chain.invoke({"transcript": rag_context.processed_transcript})


def generate_answer(
    question: str,
    faiss_index: FAISS,
    qa_chain,
    k: int = RETRIEVAL_TOP_K,
) -> str:
    # Recupera contexto y genera la respuesta final.
    relevant_context = retrieve(question, faiss_index, k=k)
    context_text = format_documents_for_prompt(relevant_context)
    return qa_chain.invoke({"context": context_text, "question": question})


def answer_question(video_url: str, user_question: str) -> str:
    # Responde una pregunta del usuario a partir del transcript indexado.
    rag_context = build_youtube_rag_context(video_url)
    if not rag_context:
        return "Please provide a valid YouTube URL with a supported local transcript."

    if not user_question:
        return "Please provide a valid question."

    qa_chain = create_qa_chain()
    return generate_answer(user_question, rag_context.faiss_index, qa_chain)
