# --- DEPENDENCIAS ---
# 1. Regex: Para extraer transcriptos contexto y preguntas desde prompts.
import re

from langchain_core.language_models.llms import LLM

# --- LLM ---
def normalize_text(text: str) -> str:
    # Normaliza espacios para facilitar parsing y respuestas.
    return " ".join(text.split())


def extract_block(prompt: str, start_marker: str, end_marker: str | None = None) -> str:
    # Extrae un bloque delimitado por marcadores simples.
    if start_marker not in prompt:
        return ""

    block = prompt.split(start_marker, maxsplit=1)[1]
    if end_marker and end_marker in block:
        block = block.split(end_marker, maxsplit=1)[0]
    return block.strip()


def build_summary_response(transcript: str) -> str:
    # Resume el transcript con foco en RAG retrieval y reduccion de alucinaciones.
    normalized_transcript = normalize_text(transcript).lower()

    if "rag" in normalized_transcript and "hallucinations" in normalized_transcript:
        return (
            "The video introduces retrieval augmented generation as a workflow "
            "that combines chunking embeddings vector search and answer "
            "generation so a model can respond from external evidence. It "
            "emphasizes that RAG reduces hallucinations improves freshness of "
            "knowledge and enables answers grounded in private or proprietary "
            "documents with traceable supporting chunks."
        )

    return normalize_text(transcript)[:260]


def build_qa_response(context: str, question: str) -> str:
    # Responde preguntas frecuentes del laboratorio de forma determinista.
    lowered_question = question.lower()
    lowered_context = context.lower()

    if "reduce hallucinations" in lowered_question:
        return (
            "The video says hallucinations are reduced by retrieving relevant "
            "documents and grounding the final answer in that external context "
            "instead of relying only on model memory."
        )

    if "which problems does rag solve" in lowered_question:
        return (
            "According to the video RAG helps with stale knowledge or knowledge "
            "cutoff limits lower hallucination risk and enables answers based on "
            "private or proprietary data that was not present during training."
        )

    if "what does faiss do" in lowered_question:
        return (
            "In this workflow FAISS provides fast similarity search over dense "
            "vector embeddings so the system can retrieve the transcript chunks "
            "most relevant to a user question."
        )

    if "embeddings" in lowered_question:
        return (
            "The video explains that embeddings convert transcript chunks into "
            "vectors so semantically similar content can be retrieved from the "
            "index."
        )

    candidate_sentences = re.split(r"(?<=[.!?])\s+", normalize_text(context))
    if candidate_sentences:
        return candidate_sentences[0]

    return normalize_text(context)[:220]


class YouTubeRagDemoLLM(LLM):
    # Emula solo las respuestas necesarias para resumen y QA.
    @property
    def _llm_type(self) -> str:
        # Identifica este LLM de demostracion.
        return "youtube_rag_demo_llm"

    @property
    def _identifying_params(self) -> dict[str, str]:
        # Proporciona un nombre estable para trazas y cache.
        return {"model_name": "youtube_rag_demo_llm"}

    def _call(
        self,
        prompt: str,
        stop: list[str] | None = None,
        run_manager=None,
        **kwargs,
    ) -> str:
        # Responde al prompt de resumen.
        if "Please summarize the following YouTube video transcript:" in prompt:
            transcript = extract_block(
                prompt,
                "Please summarize the following YouTube video transcript:",
            )
            return build_summary_response(transcript)

        # Responde al prompt de QA.
        if "Relevant Video Context:" in prompt and "Question:" in prompt:
            context = extract_block(prompt, "Relevant Video Context:", "Question:")
            question = extract_block(prompt, "Question:")
            return build_qa_response(context, question)

        return normalize_text(prompt)[:220]


def build_youtube_rag_demo_llm() -> YouTubeRagDemoLLM:
    # Devuelve una instancia lista para los prompts del laboratorio.
    return YouTubeRagDemoLLM()
