# --- DEPENDENCIAS ---
# 1. Configuracion: Para leer lineas del resumen del cheat sheet.
# 2. Datos: Para cargar filtros y consultas de ejemplo.
# 3. Coleccion: Para crear poblar y modificar la demo de ChromaDB.
# 4. Consultas: Para ejecutar filtros similarity search y lecturas por id.
from config.chromadb_cheat_sheet_config import CRUD_DEMO_ID
from config.chromadb_cheat_sheet_config import METRIC_SUMMARY_LINES
from config.chromadb_cheat_sheet_config import RAG_PIPELINE_LINES
from config.chromadb_cheat_sheet_config import RAG_PITFALL_LINES
from config.chromadb_cheat_sheet_config import RAG_RESPONSIBILITY_LINES
from config.chromadb_cheat_sheet_config import RAG_SUMMARY_LINES
from config.chromadb_cheat_sheet_config import RECOMMENDATION_SUMMARY_LINES
from config.chromadb_cheat_sheet_config import VECTOR_DATABASE_SUMMARY_LINES
from data.chromadb_demo_dataset import BASIC_QUERY_TEXT
from data.chromadb_demo_dataset import CASE_SENSITIVE_TEXT
from data.chromadb_demo_dataset import CASE_SENSITIVE_TEXT_EXPECTED
from data.chromadb_demo_dataset import COMPLEX_METADATA_FILTER
from data.chromadb_demo_dataset import CRUD_DEMO_ITEM
from data.chromadb_demo_dataset import DOCUMENT_FILTER
from data.chromadb_demo_dataset import DOCUMENT_FILTER_NEGATIVE
from data.chromadb_demo_dataset import METADATA_FILTER
from data.chromadb_demo_dataset import RAG_QUERY_TEXT
from data.chromadb_demo_dataset import RECOMMENDATION_QUERY_TEXT
from data.chromadb_demo_dataset import TECH_QUERY_TEXT
from orchestration.chromadb_collection_orchestration import add_crud_demo_item
from orchestration.chromadb_collection_orchestration import bootstrap_demo_collection
from orchestration.chromadb_collection_orchestration import delete_crud_demo_item
from orchestration.chromadb_collection_orchestration import get_existing_collection
from orchestration.chromadb_collection_orchestration import modify_collection_metadata
from orchestration.chromadb_collection_orchestration import update_crud_demo_item
from orchestration.chromadb_query_orchestration import format_get_result
from orchestration.chromadb_query_orchestration import format_query_result
from orchestration.chromadb_query_orchestration import get_all_documents
from orchestration.chromadb_query_orchestration import get_documents_by_id
from orchestration.chromadb_query_orchestration import (
    get_documents_with_document_filter,
)
from orchestration.chromadb_query_orchestration import (
    get_documents_with_metadata_filter,
)
from orchestration.chromadb_query_orchestration import query_by_text

# --- RUNNER ---
# 1.1. Funcion para imprimir titulos de seccion en consola.
def print_section(title: str):
    # Separa visualmente cada bloque de la practica.
    print(f"\n=== {title} ===")


# 1.2. Funcion para imprimir una lista simple de lineas.
def print_lines(lines: list[str]):
    # Recorre cada linea y la imprime en consola.
    for line in lines:
        print(f"- {line}")


# 1.3. Funcion para ejecutar el resumen y la demo de ChromaDB.
def run_chromadb_cheat_sheet_lab():
    # Muestra el bloque inicial de metricas vectoriales.
    print("Practica 06 Introduction to Vector Databases and Chroma DB Cheat Sheet.")
    print_section("Distance And Similarity Metrics")
    print_lines(METRIC_SUMMARY_LINES)
    print_section("RAG Overview")
    print_lines(RAG_SUMMARY_LINES)
    print_section("RAG Pipeline")
    print_lines(RAG_PIPELINE_LINES)
    print_section("Vector Database Responsibilities In RAG")
    print_lines(RAG_RESPONSIBILITY_LINES)
    print_section("Common RAG Pitfalls")
    print_lines(RAG_PITFALL_LINES)
    print_section("Recommendation Systems")
    print_lines(RECOMMENDATION_SUMMARY_LINES)
    print_section("Vector Databases")
    print_lines(VECTOR_DATABASE_SUMMARY_LINES)

    # Construye una coleccion local y la carga con datos de ejemplo.
    collection = bootstrap_demo_collection()
    collection = get_existing_collection()
    modify_collection_metadata(
        collection,
        {"topic": "query testing", "mode": "cheat sheet", "domain": "rag"},
    )

    print_section("All Documents")
    print(format_get_result(get_all_documents(collection)))

    print_section("Metadata Filter")
    print(format_get_result(get_documents_with_metadata_filter(collection, METADATA_FILTER)))

    print_section("Complex Metadata Filter")
    print(
        format_get_result(
            get_documents_with_metadata_filter(collection, COMPLEX_METADATA_FILTER)
        )
    )

    print_section("Document Filter Case Sensitive")
    print(f"Busqueda con texto exacto esperado: {CASE_SENSITIVE_TEXT_EXPECTED}")
    print(format_get_result(get_documents_with_document_filter(collection, DOCUMENT_FILTER)))
    print(f"Busqueda con mayuscula distinta: {CASE_SENSITIVE_TEXT}")
    print(
        format_get_result(
            get_documents_with_document_filter(
                collection,
                {"$contains": CASE_SENSITIVE_TEXT},
            )
        )
    )

    print_section("Document Filter Negative")
    print(
        format_get_result(
            get_documents_with_document_filter(collection, DOCUMENT_FILTER_NEGATIVE)
        )
    )

    print_section("Similarity Search")
    print(f"Query: {BASIC_QUERY_TEXT}")
    print(format_query_result(query_by_text(collection, BASIC_QUERY_TEXT)))

    print_section("RAG Query Example")
    print(f"Query: {RAG_QUERY_TEXT}")
    print(format_query_result(query_by_text(collection, RAG_QUERY_TEXT)))

    print_section("Similarity Search With Filters")
    print(f"Query: {TECH_QUERY_TEXT}")
    print(
        format_query_result(
            query_by_text(
                collection,
                TECH_QUERY_TEXT,
                where_filter=COMPLEX_METADATA_FILTER,
                where_document={"$not_contains": "vector"},
            )
        )
    )

    print_section("Recommendation Query")
    print(f"Query: {RECOMMENDATION_QUERY_TEXT}")
    print(format_query_result(query_by_text(collection, RECOMMENDATION_QUERY_TEXT)))

    print_section("CRUD Operations")
    add_crud_demo_item(collection)
    print(f"Added: {CRUD_DEMO_ITEM['id']}")
    print(format_get_result(get_documents_by_id(collection, [CRUD_DEMO_ID])))

    updated_document, updated_metadata = update_crud_demo_item(collection)
    print("Updated:")
    print(updated_metadata)
    print(updated_document)
    print(format_get_result(get_documents_by_id(collection, [CRUD_DEMO_ID])))

    delete_crud_demo_item(collection)
    print("Deleted:")
    print(format_get_result(get_documents_by_id(collection, [CRUD_DEMO_ID])))
