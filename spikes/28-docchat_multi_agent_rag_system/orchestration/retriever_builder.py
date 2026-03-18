# --- DEPENDENCIAS ---
import shutil

from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

from config.docchat_config import CHROMA_DB_PATH
from config.docchat_config import HYBRID_RETRIEVER_WEIGHTS
from config.docchat_config import VECTOR_SEARCH_K
from models.docchat_embedding_gateway import build_docchat_embeddings


class RetrieverBuilder:
    def __init__(self, embeddings=None):
        self.embeddings = embeddings or build_docchat_embeddings()

    def build_hybrid_retriever(self, docs: list[Document]):
        if CHROMA_DB_PATH.exists():
            shutil.rmtree(CHROMA_DB_PATH, ignore_errors=True)
        CHROMA_DB_PATH.mkdir(parents=True, exist_ok=True)

        vector_store = Chroma.from_documents(
            documents=docs,
            embedding=self.embeddings,
            persist_directory=str(CHROMA_DB_PATH),
        )
        bm25 = BM25Retriever.from_documents(docs)
        vector_retriever = vector_store.as_retriever(search_kwargs={"k": VECTOR_SEARCH_K})
        return EnsembleRetriever(
            retrievers=[bm25, vector_retriever],
            weights=HYBRID_RETRIEVER_WEIGHTS,
        )