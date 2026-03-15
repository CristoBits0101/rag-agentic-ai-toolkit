# --- DEPENDENCIAS ---
# 1. Contextlib: Para silenciar salida ruidosa del indexado de resumenes.
# 2. Dataclass: Para transportar el estado del laboratorio.
# 3. Functools: Para cachear los componentes del spike.
# 4. Io: Para capturar stdout temporalmente.
from contextlib import redirect_stdout
from dataclasses import dataclass
from functools import lru_cache
import io

from llama_index.core import Document
from llama_index.core import DocumentSummaryIndex
from llama_index.core import KeywordTableIndex
from llama_index.core import Settings
from llama_index.core import StorageContext
from llama_index.core import VectorStoreIndex
from llama_index.core.node_parser import HierarchicalNodeParser
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.node_parser import get_leaf_nodes
from llama_index.core.retrievers import RecursiveRetriever
from llama_index.core.schema import IndexNode
from llama_index.core.storage.docstore import SimpleDocumentStore

from config.advanced_retrievers_config import HIERARCHICAL_CHUNK_OVERLAP
from config.advanced_retrievers_config import HIERARCHICAL_CHUNK_SIZES
from config.advanced_retrievers_config import SIMILARITY_TOP_K
from data.advanced_retrievers_documents import LONG_FORM_DOCUMENTS
from data.advanced_retrievers_documents import RECURSIVE_TOPIC_DOCUMENTS
from data.advanced_retrievers_documents import SAMPLE_DOCUMENTS
from models.advanced_retrievers_demo_llm import build_advanced_retrievers_demo_llm
from models.llamaindex_demo_embedding_gateway import (
    build_advanced_retrievers_demo_embedding,
)

# --- MODELOS ---
@dataclass(frozen=True)
class AdvancedRetrieversLabContext:
    documents: list[Document]
    nodes: list
    vector_index: VectorStoreIndex
    document_summary_index: DocumentSummaryIndex
    keyword_index: KeywordTableIndex


@dataclass(frozen=True)
class AutoMergingBundle:
    leaf_retriever: object
    storage_context: StorageContext


@dataclass(frozen=True)
class RecursiveBundle:
    recursive_retriever: RecursiveRetriever


def configure_demo_settings():
    # Configura el LLM y los embeddings de demostracion.
    Settings.llm = build_advanced_retrievers_demo_llm()
    Settings.embed_model = build_advanced_retrievers_demo_embedding()


def build_sample_documents() -> list[Document]:
    # Convierte el dataset base en documentos de LlamaIndex.
    return [
        Document(
            text=record["text"],
            metadata={"title": record["title"], "topic": record["topic"]},
        )
        for record in SAMPLE_DOCUMENTS
    ]


def build_long_form_documents() -> list[Document]:
    # Convierte el dataset jerarquico en documentos de LlamaIndex.
    return [
        Document(
            text=record["text"],
            metadata={"title": record["title"], "topic": record["topic"]},
        )
        for record in LONG_FORM_DOCUMENTS
    ]


@lru_cache(maxsize=1)
def build_advanced_retrievers_lab_context() -> AdvancedRetrieversLabContext:
    # Crea documentos nodos e indices base del laboratorio.
    configure_demo_settings()
    documents = build_sample_documents()
    nodes = SentenceSplitter(chunk_size=160, chunk_overlap=20).get_nodes_from_documents(
        documents
    )
    vector_index = VectorStoreIndex.from_documents(documents)

    with redirect_stdout(io.StringIO()):
        document_summary_index = DocumentSummaryIndex.from_documents(documents)

    keyword_index = KeywordTableIndex.from_documents(documents)
    return AdvancedRetrieversLabContext(
        documents=documents,
        nodes=nodes,
        vector_index=vector_index,
        document_summary_index=document_summary_index,
        keyword_index=keyword_index,
    )


@lru_cache(maxsize=1)
def build_auto_merging_bundle() -> AutoMergingBundle:
    # Construye el storage jerarquico para auto merging.
    configure_demo_settings()
    documents = build_long_form_documents()
    parser = HierarchicalNodeParser.from_defaults(
        chunk_sizes=HIERARCHICAL_CHUNK_SIZES,
        chunk_overlap=HIERARCHICAL_CHUNK_OVERLAP,
    )
    hierarchical_nodes = parser.get_nodes_from_documents(documents)
    leaf_nodes = get_leaf_nodes(hierarchical_nodes)
    docstore = SimpleDocumentStore()
    docstore.add_documents(hierarchical_nodes)
    storage_context = StorageContext.from_defaults(docstore=docstore)
    vector_index = VectorStoreIndex(leaf_nodes, storage_context=storage_context)
    leaf_retriever = vector_index.as_retriever(similarity_top_k=SIMILARITY_TOP_K + 3)
    return AutoMergingBundle(
        leaf_retriever=leaf_retriever,
        storage_context=storage_context,
    )


@lru_cache(maxsize=1)
def build_recursive_bundle() -> RecursiveBundle:
    # Construye un recursive retriever con dos niveles de referencias.
    configure_demo_settings()
    retriever_dict = {}

    for topic_name, records in RECURSIVE_TOPIC_DOCUMENTS.items():
        topic_documents = [
            Document(text=record["text"], metadata={"title": record["title"]})
            for record in records
        ]
        topic_index = VectorStoreIndex.from_documents(topic_documents)
        retriever_dict[topic_name] = topic_index.as_retriever(similarity_top_k=2)

    root_nodes = [
        IndexNode(
            text=(
                "Learning retriever covers supervised learning unsupervised "
                "learning reinforcement learning transfer learning and deep "
                "learning."
            ),
            index_id="learning",
        ),
        IndexNode(
            text=(
                "Applications retriever covers AI applications in assistants "
                "computer vision translation automation and enterprise systems."
            ),
            index_id="applications",
        ),
    ]
    root_index = VectorStoreIndex(root_nodes)
    retriever_dict["root"] = root_index.as_retriever(similarity_top_k=1)
    recursive_retriever = RecursiveRetriever(
        "root",
        retriever_dict=retriever_dict,
        query_engine_dict={},
        verbose=False,
    )
    return RecursiveBundle(recursive_retriever=recursive_retriever)
