# --- DEPENDENCIAS ---
# 1. Configuracion: Para leer lineas del resumen del cheat sheet.
# 2. Datos: Para cargar filtros y consultas de ejemplo.
# 3. Coleccion: Para crear y poblar la demo de ChromaDB.
# 4. Consultas: Para ejecutar filtros y similarity search.
from config.chromadb_cheat_sheet_config import METRIC_SUMMARY_LINES
from config.chromadb_cheat_sheet_config import VECTOR_DATABASE_SUMMARY_LINES
from data.chromadb_demo_dataset import BASIC_QUERY_TEXT
from data.chromadb_demo_dataset import CASE_SENSITIVE_TEXT
from data.chromadb_demo_dataset import CASE_SENSITIVE_TEXT_EXPECTED
from data.chromadb_demo_dataset import COMPLEX_METADATA_FILTER
from data.chromadb_demo_dataset import DOCUMENT_FILTER
from data.chromadb_demo_dataset import DOCUMENT_FILTER_NEGATIVE
from data.chromadb_demo_dataset import METADATA_FILTER
from data.chromadb_demo_dataset import TECH_QUERY_TEXT
from orchestration.chromadb_collection_orchestration import bootstrap_demo_collection
from orchestration.chromadb_query_orchestration import format_get_result
from orchestration.chromadb_query_orchestration import format_query_result
from orchestration.chromadb_query_orchestration import get_all_documents
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
    print_section("Vector Databases")
    print_lines(VECTOR_DATABASE_SUMMARY_LINES)

    # Construye una coleccion local y la carga con datos de ejemplo.
    collection = bootstrap_demo_collection()

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
