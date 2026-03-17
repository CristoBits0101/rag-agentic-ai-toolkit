# --- DEPENDENCIAS ---
import json
from functools import lru_cache
from urllib.error import HTTPError
from urllib.error import URLError
from urllib.request import Request
from urllib.request import urlopen

from llama_index.core.base.embeddings.base import BaseEmbedding
from llama_index.core.llms import CompletionResponse
from llama_index.core.llms import CompletionResponseGen
from llama_index.core.llms import CustomLLM
from llama_index.core.llms import LLMMetadata
from llama_index.core.llms.callbacks import llm_completion_callback

try:
    from langchain_ollama import OllamaEmbeddings
except Exception:
    OllamaEmbeddings = None

OLLAMA_API_URL = "http://127.0.0.1:11434/api/generate"
OLLAMA_TEXT_MODEL_NAME = "qwen2.5:7b"
OLLAMA_EMBEDDING_MODEL_NAME = "nomic-embed-text"


def send_ollama_generate_request(
    prompt: str,
    model_name: str = OLLAMA_TEXT_MODEL_NAME,
    api_url: str = OLLAMA_API_URL,
) -> str:
    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0},
    }
    request = Request(
        api_url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Accept": "application/json", "Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urlopen(request, timeout=120) as response:
            response_payload = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        raise RuntimeError(f"Ollama generate endpoint returned HTTP {exc.code}.") from exc
    except URLError as exc:
        raise RuntimeError("Ollama could not be reached. Verify ollama serve is running.") from exc
    except Exception as exc:
        raise RuntimeError("Ollama generate endpoint returned an invalid response.") from exc

    content = str(response_payload.get("response", "")).strip()
    if not content:
        raise RuntimeError(
            f"Ollama returned an empty response for model {model_name}. Verify the model is installed."
        )

    return content


@lru_cache(maxsize=1)
def get_ollama_embedding_model():
    if OllamaEmbeddings is None:
        raise RuntimeError(
            "LangChain Ollama is not available. Install langchain-ollama before running practica 10."
        )

    return OllamaEmbeddings(model=OLLAMA_EMBEDDING_MODEL_NAME)


class AdvancedRetrieversOllamaEmbedding(BaseEmbedding):
    model_name: str = OLLAMA_EMBEDDING_MODEL_NAME

    def _get_query_embedding(self, query: str) -> list[float]:
        return get_ollama_embedding_model().embed_query(query)

    async def _aget_query_embedding(self, query: str) -> list[float]:
        return self._get_query_embedding(query)

    def _get_text_embedding(self, text: str) -> list[float]:
        return get_ollama_embedding_model().embed_query(text)

    def _get_text_embeddings(self, texts: list[str]) -> list[list[float]]:
        return get_ollama_embedding_model().embed_documents(texts)


class AdvancedRetrieversOllamaLLM(CustomLLM):
    @property
    def metadata(self) -> LLMMetadata:
        return LLMMetadata(
            context_window=8192,
            num_output=512,
            model_name=OLLAMA_TEXT_MODEL_NAME,
        )

    @llm_completion_callback()
    def complete(
        self,
        prompt: str,
        formatted: bool = False,
        **kwargs,
    ) -> CompletionResponse:
        return CompletionResponse(text=send_ollama_generate_request(prompt))

    @llm_completion_callback()
    def stream_complete(
        self,
        prompt: str,
        formatted: bool = False,
        **kwargs,
    ) -> CompletionResponseGen:
        response = self.complete(prompt, formatted=formatted, **kwargs)
        yield CompletionResponse(text=response.text, delta=response.text)


def build_advanced_retrievers_llm() -> AdvancedRetrieversOllamaLLM:
    return AdvancedRetrieversOllamaLLM()


def build_advanced_retrievers_embedding() -> AdvancedRetrieversOllamaEmbedding:
    return AdvancedRetrieversOllamaEmbedding()
