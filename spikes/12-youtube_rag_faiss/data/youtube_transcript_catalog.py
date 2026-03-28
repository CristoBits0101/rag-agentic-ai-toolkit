# --- DEPENDENCIAS ---
# 1. Dataclass: Para representar cada segmento del transcript.
from dataclasses import dataclass


@dataclass(frozen=True)
class TranscriptSegment:
    text: str
    start: float
    duration: float


YOUTUBE_TRANSCRIPT_CATALOG = {
    "T-D1OfcDW1M": [
        TranscriptSegment(
            text="Welcome to this overview of retrieval augmented generation or RAG.",
            start=0.0,
            duration=4.0,
        ),
        TranscriptSegment(
            text="RAG combines retrieval and text generation so a language model can answer from external evidence instead of relying only on training memory.",
            start=4.2,
            duration=6.0,
        ),
        TranscriptSegment(
            text="A base language model can hallucinate when facts are missing stale or too domain specific.",
            start=10.8,
            duration=4.5,
        ),
        TranscriptSegment(
            text="To reduce hallucinations you retrieve relevant documents and ground the answer in that context.",
            start=15.6,
            duration=4.0,
        ),
        TranscriptSegment(
            text="This helps with knowledge cutoff problems and with private company data that the model never saw during training.",
            start=20.0,
            duration=4.8,
        ),
        TranscriptSegment(
            text="The first step is document ingestion where files or notes are split into chunks that remain small enough for retrieval.",
            start=25.2,
            duration=5.2,
        ),
        TranscriptSegment(
            text="Next each chunk is converted into embeddings so semantically similar content lands close together in vector space.",
            start=30.8,
            duration=5.0,
        ),
        TranscriptSegment(
            text="A vector index stores those embeddings and lets us search for the nearest chunks to a user question.",
            start=36.2,
            duration=4.6,
        ),
        TranscriptSegment(
            text="FAISS is one tool for that step because it performs fast similarity search over dense vectors.",
            start=41.0,
            duration=4.3,
        ),
        TranscriptSegment(
            text="When the user asks a question the retriever finds the most relevant chunks and passes them to the model as grounded context.",
            start=45.7,
            duration=5.0,
        ),
        TranscriptSegment(
            text="The generator then produces an answer that is more precise traceable and aligned with the retrieved source material.",
            start=51.1,
            duration=4.7,
        ),
        TranscriptSegment(
            text="RAG is useful when you need fresher information lower hallucination risk and answers based on proprietary data.",
            start=56.2,
            duration=4.8,
        ),
        TranscriptSegment(
            text="It also improves transparency because the application can show the exact chunks used to support the final response.",
            start=61.4,
            duration=4.6,
        ),
        TranscriptSegment(
            text="In practice a RAG pipeline often includes chunking embeddings vector storage retrieval prompt assembly and final answer generation.",
            start=66.3,
            duration=5.2,
        ),
    ]
}
