# --- DEPENDENCIAS ---
# 1. Json: Para serializar respuestas estructuradas validas.
# 2. Regex: Para extraer la consulta actual del prompt de Self Query.
import json
import re

from langchain_core.language_models.llms import LLM

# --- LLM ---
def extract_user_query_from_prompt(prompt: str) -> str:
    # Toma la ultima consulta de usuario del prompt few shot.
    matches = re.findall(
        r"User Query:\n(.*?)\n\nStructured Request:",
        prompt,
        flags=re.DOTALL,
    )

    if not matches:
        return ""

    return matches[-1].strip()


def build_multi_query_response(question: str) -> str:
    # Crea variantes simples y deterministas para ampliar recall.
    normalized_question = question.strip()
    lowered_question = normalized_question.lower()

    if "langchain" in lowered_question:
        return "\n".join(
            [
                "What does the paper explain about LangChain retrievers?",
                "How does the paper describe MultiQueryRetriever in LangChain?",
                "What LangChain retrieval components are discussed in the paper?",
            ]
        )

    return "\n".join(
        [
            normalized_question,
            f"Explain {normalized_question.lower()}",
            f"Summarize the key retrieval ideas behind {normalized_question.lower()}",
        ]
    )


def build_self_query_payload(user_query: str) -> dict[str, str]:
    # Traduce unas pocas consultas conocidas al esquema estructurado.
    lowered_query = user_query.lower()

    if "higher than 8.5" in lowered_query:
        return {
            "query": "",
            "filter": 'gt("rating", 8.5)',
        }

    if "greta gerwig" in lowered_query:
        return {
            "query": "women",
            "filter": 'eq("director", "Greta Gerwig")',
        }

    if "science fiction" in lowered_query and "highly rated" in lowered_query:
        return {
            "query": "science fiction",
            "filter": 'and(gt("rating", 8.5), eq("genre", "science fiction"))',
        }

    return {
        "query": user_query,
        "filter": "NO_FILTER",
    }


class ContextRetrievalDemoLLM(LLM):
    # Emula solo las respuestas necesarias para el laboratorio.
    @property
    def _llm_type(self) -> str:
        # Identifica este LLM de demostracion.
        return "context_retrieval_demo_llm"

    @property
    def _identifying_params(self) -> dict[str, str]:
        # Proporciona un nombre estable para trazas y cache.
        return {"model_name": "context_retrieval_demo_llm"}

    def _call(
        self,
        prompt: str,
        stop: list[str] | None = None,
        run_manager=None,
        **kwargs,
    ) -> str:
        # Responde al prompt de expansion de consultas.
        if "Original question:" in prompt:
            question = prompt.split("Original question:", maxsplit=1)[1].strip()
            return build_multi_query_response(question)

        # Responde al prompt del Self Query constructor.
        user_query = extract_user_query_from_prompt(prompt)
        payload = build_self_query_payload(user_query)
        return f"```json\n{json.dumps(payload)}\n```"


def build_context_retrieval_demo_llm() -> ContextRetrievalDemoLLM:
    # Devuelve una instancia lista para retrievers que dependen de LLM.
    return ContextRetrievalDemoLLM()
