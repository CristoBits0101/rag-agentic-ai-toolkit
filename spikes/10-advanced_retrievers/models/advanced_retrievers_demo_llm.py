# --- DEPENDENCIAS ---
# 1. Regex: Para extraer bloques del prompt.
import re

from llama_index.core.llms import CompletionResponse
from llama_index.core.llms import CompletionResponseGen
from llama_index.core.llms import CustomLLM
from llama_index.core.llms import LLMMetadata
from llama_index.core.llms.callbacks import llm_completion_callback

from models.llamaindex_demo_embedding_gateway import KEYWORD_GROUPS
from models.llamaindex_demo_embedding_gateway import tokenize_text

# --- LLM ---
SUMMARY_PROFILES = [
    (
        "ml_basics",
        {
            "artificial intelligence",
            "forecasting",
            "machine learning",
            "patterns from data",
            "recommendation",
        },
        "This document introduces machine learning fundamentals. "
        "It can answer questions about learning from data and core ML tasks.",
    ),
    (
        "supervised_learning",
        {
            "classification",
            "labeled",
            "prediction",
            "regression",
            "supervised",
        },
        "This document explains supervised learning with labeled data. "
        "It can answer questions about classification regression and prediction.",
    ),
    (
        "unsupervised_learning",
        {
            "anomaly",
            "clustering",
            "structure",
            "unlabeled",
            "unsupervised",
        },
        "This document explains unsupervised learning with unlabeled data. "
        "It can answer questions about clustering anomaly detection and discovery.",
    ),
    (
        "reinforcement_learning",
        {
            "agents",
            "policies",
            "reinforcement",
            "rewards",
            "robotics",
        },
        "This document explains reinforcement learning for sequential decisions. "
        "It can answer questions about agents rewards policies and robotics.",
    ),
    (
        "transfer_learning",
        {"adaptation", "pretrained", "reuse", "transfer"},
        "This document explains transfer learning with pretrained models. "
        "It can answer questions about adaptation and data efficiency.",
    ),
    (
        "deep_learning",
        {
            "backpropagation",
            "deep",
            "hidden",
            "neural",
            "network",
            "networks",
        },
        "This document explains deep learning and neural networks. "
        "It can answer questions about layered models backpropagation and training.",
    ),
    (
        "nlp",
        {
            "chatbots",
            "enterprise search",
            "natural language processing",
            "summarize",
            "translate",
        },
        "This document explains natural language processing. "
        "It can answer questions about translation assistants search and text understanding.",
    ),
    (
        "computer_vision",
        {
            "computer vision",
            "image",
            "imaging",
            "pixels",
            "video",
        },
        "This document explains computer vision. "
        "It can answer questions about image analysis detection and visual understanding.",
    ),
    (
        "applications",
        {
            "applications",
            "assistants",
            "automation",
            "inspection",
            "translation",
            "vision",
        },
        "This document surveys AI applications in language vision and assistants. "
        "It can answer questions about enterprise use cases and automation.",
    ),
    (
        "generative_ai",
        {"creates new text", "generative ai", "images", "synthetic media"},
        "This document explains generative AI. "
        "It can answer questions about content generation code generation and creative workflows.",
    ),
    (
        "llm",
        {
            "code generation",
            "large language models",
            "massive text corpora",
            "question answering",
            "summarization",
        },
        "This document explains large language models. "
        "It can answer questions about reasoning summarization and generative AI assistants.",
    ),
    (
        "hybrid_retrieval",
        {"bm25", "fusion", "hybrid", "keyword", "retrieval", "vector"},
        "This document explains hybrid retrieval. "
        "It can answer questions about BM25 vector search and query fusion.",
    ),
]


def normalize_text(text: str) -> str:
    # Limpia espacios y deja el texto en una sola linea.
    return " ".join(text.split())


def score_text_against_query(query: str, text: str) -> int:
    # Combina overlap directo y overlap por grupos del dominio.
    query_tokens = set(tokenize_text(query))
    text_tokens = set(tokenize_text(text))
    score = len(query_tokens & text_tokens)

    for keywords in KEYWORD_GROUPS.values():
        if query_tokens & keywords and text_tokens & keywords:
            score += 2

    if "learning" in query_tokens and text_tokens & {
        "supervised",
        "unsupervised",
        "reinforcement",
        "transfer",
    }:
        score += 3

    if "applications" in query_tokens and text_tokens & {
        "applications",
        "assistants",
        "automation",
        "translation",
        "vision",
    }:
        score += 3

    return score


def build_summary_from_context(context: str) -> str:
    # Resume el contexto segun la señal dominante del texto.
    cleaned_context = normalize_text(context)
    lowered_context = cleaned_context.lower()
    best_summary = (
        f"{cleaned_context[:180]} "
        "It can answer questions about the main topic and common uses."
    )
    best_score = -1

    for _, keywords, summary in SUMMARY_PROFILES:
        current_score = sum(keyword in lowered_context for keyword in keywords)
        if current_score > best_score:
            best_score = current_score
            best_summary = summary

    return best_summary


def build_query_variations(query: str) -> str:
    # Genera reformulaciones deterministas para fusion.
    lowered_query = query.lower()

    if "main approaches to machine learning" in lowered_query:
        return "\n".join(
            [
                "supervised unsupervised reinforcement and transfer learning",
                "machine learning methods and learning paradigms",
                "types of machine learning used in AI systems",
            ]
        )

    if "applications of ai" in lowered_query:
        return "\n".join(
            [
                "ai applications in language vision and assistants",
                "enterprise use cases for ai systems",
                "how ai is used in production workflows",
            ]
        )

    normalized_query = query.strip()
    return "\n".join(
        [
            normalized_query,
            f"Explain {normalized_query.lower()}",
            f"Key concepts behind {normalized_query.lower()}",
        ]
    )


def parse_document_blocks(prompt: str) -> list[tuple[int, str]]:
    # Extrae las opciones de resumen del prompt de seleccion.
    prompt_body = prompt.rsplit("Let's try this now:", maxsplit=1)[-1]
    matches = re.findall(
        r"Document\s+(\d+):\n(.*?)(?=\nDocument\s+\d+:\n|\nQuestion:)",
        prompt_body,
        flags=re.DOTALL,
    )
    return [(int(index), normalize_text(text)) for index, text in matches]


def parse_question(prompt: str) -> str:
    # Obtiene la consulta principal desde el prompt.
    if "Question:" in prompt:
        question_block = prompt.rsplit("Question:", maxsplit=1)[1]
        return normalize_text(question_block.split("Answer:", maxsplit=1)[0])

    if "Query:" in prompt and "Queries:" in prompt:
        query_block = prompt.rsplit("Query:", maxsplit=1)[1]
        return normalize_text(query_block.split("Queries:", maxsplit=1)[0])

    if "Query:" in prompt:
        query_block = prompt.rsplit("Query:", maxsplit=1)[1]
        return normalize_text(query_block.split("Answer:", maxsplit=1)[0])

    return ""


def build_choice_response(prompt: str) -> str:
    # Selecciona documentos segun relevancia determinista.
    question = parse_question(prompt)
    ranked_blocks = []

    for index, summary in parse_document_blocks(prompt):
        score = score_text_against_query(question, summary)
        if score > 0:
            ranked_blocks.append((index, min(10, score + 2), summary))

    if not ranked_blocks:
        return "Doc: 1, Relevance: 1"

    ranked_blocks.sort(key=lambda item: (-item[1], item[0]))
    return "\n".join(
        f"Doc: {index}, Relevance: {relevance}"
        for index, relevance, _ in ranked_blocks[:3]
    )


def extract_context(prompt: str) -> str:
    # Obtiene el bloque central de contexto de prompts de sintesis.
    matches = re.findall(
        r"---------------------\n(.*?)\n---------------------",
        prompt,
        flags=re.DOTALL,
    )
    return normalize_text(" ".join(matches))


def build_context_answer(prompt: str) -> str:
    # Genera una respuesta breve usando las frases mas relevantes del contexto.
    query = parse_question(prompt)
    context = extract_context(prompt)
    lowered_query = query.lower()
    lowered_context = context.lower()

    if "Describe what the provided text is about" in query:
        return build_summary_from_context(context)

    if "main approaches to machine learning" in lowered_query:
        approaches = [
            label
            for label in [
                "supervised learning",
                "unsupervised learning",
                "reinforcement learning",
                "transfer learning",
                "deep learning",
            ]
            if label in lowered_context
        ]
        if approaches:
            listed_approaches = ", ".join(approaches)
            return f"The main approaches to machine learning in this context are {listed_approaches}."

    candidate_sentences = re.split(r"(?<=[.!?])\s+", context)
    scored_sentences = [
        (score_text_against_query(query, sentence), normalize_text(sentence))
        for sentence in candidate_sentences
        if sentence.strip()
    ]
    scored_sentences.sort(key=lambda item: item[0], reverse=True)
    best_sentences = [sentence for score, sentence in scored_sentences if score > 0][:2]

    if not best_sentences:
        return context[:220]

    return " ".join(best_sentences)


class AdvancedRetrieversDemoLLM(CustomLLM):
    # Responde a los prompts necesarios para el laboratorio.
    @property
    def metadata(self) -> LLMMetadata:
        # Expone metadatos minimos para LlamaIndex.
        return LLMMetadata(
            context_window=4096,
            num_output=256,
            model_name="advanced_retrievers_demo_llm",
        )

    @llm_completion_callback()
    def complete(
        self,
        prompt: str,
        formatted: bool = False,
        **kwargs,
    ) -> CompletionResponse:
        # Resuelve fusion de consultas seleccion de resumenes y sintesis.
        if "You are a helpful assistant that generates multiple search queries" in prompt:
            return CompletionResponse(text=build_query_variations(parse_question(prompt)))

        if "A list of documents is shown below." in prompt:
            return CompletionResponse(text=build_choice_response(prompt))

        if "Context information" in prompt and "answer the query" in prompt.lower():
            return CompletionResponse(text=build_context_answer(prompt))

        return CompletionResponse(text=normalize_text(prompt)[:220])

    @llm_completion_callback()
    def stream_complete(
        self,
        prompt: str,
        formatted: bool = False,
        **kwargs,
    ) -> CompletionResponseGen:
        # Emite la respuesta completa como unico delta.
        response = self.complete(prompt, formatted=formatted, **kwargs)
        yield CompletionResponse(text=response.text, delta=response.text)


def build_advanced_retrievers_demo_llm() -> AdvancedRetrieversDemoLLM:
    # Devuelve una instancia lista para indices y query engines.
    return AdvancedRetrieversDemoLLM()
