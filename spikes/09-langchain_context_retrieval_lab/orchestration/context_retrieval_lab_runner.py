# --- DEPENDENCIAS ---
# 1. Configuracion: Para reutilizar consultas del laboratorio.
# 2. Parent Retrieval: Para mostrar child chunks y parent docs.
# 3. Search: Para mostrar retrieval clasico y MultiQuery.
# 4. Self Query: Para mostrar filtros por metadatos.
from config.context_retrieval_config import MULTI_QUERY_QUESTION
from config.context_retrieval_config import PARENT_QUERY
from langchain_core.documents import Document
from orchestration.context_retrieval_parent_orchestration import (
    retrieve_parent_documents,
)
from orchestration.context_retrieval_search_orchestration import (
    retrieve_multi_query_documents,
)
from orchestration.context_retrieval_search_orchestration import (
    run_policy_retrieval_examples,
)
from orchestration.context_retrieval_self_query_orchestration import (
    run_self_query_examples,
)

# --- RUNNER ---
def print_section(title: str):
    # Separa visualmente cada bloque del laboratorio.
    print(f"\n=== {title} ===")


def format_document(document: Document) -> str:
    # Crea una linea compacta con metadatos y contenido.
    snippet = " ".join(document.page_content.split())[:140]

    if not document.metadata:
        return snippet

    metadata = " | ".join(f"{key}: {value}" for key, value in document.metadata.items())
    return f"{metadata} | {snippet}"


def print_documents(documents: list[Document]):
    # Recorre e imprime los documentos recuperados.
    if not documents:
        print("No documents found.")
        return

    for index, document in enumerate(documents, start=1):
        print(f"{index}. {format_document(document)}")


def run_langchain_context_retrieval_lab():
    # Ejecuta las secciones del laboratorio en el mismo orden conceptual.
    print("Practica 09 Build A Smarter Search With LangChain Context Retrieval")

    print_section("Basic Retriever Variants")
    retrieval_examples = run_policy_retrieval_examples()
    print("Similarity search for email policy.")
    print_documents(retrieval_examples["similarity"])
    print("\nTop 1 retrieval.")
    print_documents(retrieval_examples["top_k_1"])
    print("\nMMR retrieval.")
    print_documents(retrieval_examples["mmr"])
    print("\nSimilarity score threshold retrieval.")
    print_documents(retrieval_examples["threshold"])

    print_section("Multi Query Retrieval")
    print(f"Question: {MULTI_QUERY_QUESTION}")
    print_documents(retrieve_multi_query_documents())

    print_section("Self Query Retrieval")
    self_query_examples = run_self_query_examples()
    for prompt, documents in self_query_examples.items():
        print(f"\nPrompt: {prompt}")
        print_documents(documents)

    print_section("Parent Document Retrieval")
    child_documents, parent_documents, parent_key_count = retrieve_parent_documents()
    print(f"Stored parent documents: {parent_key_count}")
    print(f"Query: {PARENT_QUERY}")
    print("\nChild chunks returned by similarity search.")
    print_documents(child_documents)
    print("\nParent documents returned by the retriever.")
    print_documents(parent_documents)
