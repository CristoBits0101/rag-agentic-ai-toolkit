# --- DEPENDENCIAS ---
# 1. Numpy: Para comparar matrices y redondear valores en la salida.
# 2. Configuracion: Para leer la tolerancia numerica del laboratorio.
# 3. Datos: Para cargar documentos y consulta de ejemplo.
# 4. Metricas: Para ejecutar calculos manuales y comparativas.
# 5. Search: Para generar embeddings y resolver la consulta final.
import numpy as np

from config.similarity_runtime_config import NUMERICAL_TOLERANCE
from data.similarity_documents import DOCUMENTS
from data.similarity_documents import QUERY_TEXT
from orchestration.similarity_metrics_orchestration import build_cosine_distance_matrix
from orchestration.similarity_metrics_orchestration import build_cosine_similarity_matrix
from orchestration.similarity_metrics_orchestration import (
    build_cosine_similarity_matrix_operator,
)
from orchestration.similarity_metrics_orchestration import build_dot_product_distance_matrix
from orchestration.similarity_metrics_orchestration import build_dot_product_matrix
from orchestration.similarity_metrics_orchestration import (
    build_dot_product_matrix_operator,
)
from orchestration.similarity_metrics_orchestration import build_l2_distance_matrix
from orchestration.similarity_metrics_orchestration import build_l2_distance_matrix_improved
from orchestration.similarity_metrics_orchestration import build_l2_distance_matrix_scipy
from orchestration.similarity_metrics_orchestration import normalize_embeddings_manual
from orchestration.similarity_metrics_orchestration import normalize_embeddings_torch
from orchestration.similarity_metrics_orchestration import verify_normalized_embeddings
from orchestration.similarity_search_orchestration import generate_document_embeddings
from orchestration.similarity_search_orchestration import search_documents_by_query

# --- RUNNER ---
# 1.1. Funcion para imprimir encabezados breves en consola.
def print_section(title: str):
    # Separa cada bloque de salida para facilitar la lectura.
    print(f"\n=== {title} ===")


# 1.2. Funcion para imprimir matrices redondeadas.
def print_matrix(name: str, matrix: np.ndarray):
    # Presenta matrices con pocos decimales para salida compacta.
    print(f"{name}:\n{np.round(matrix, 4)}")


# 1.3. Funcion para ejecutar el laboratorio completo.
def run_similarity_lab():
    # Muestra la intencion general del spike.
    print("Practica 05 Similarity Search By Hand.")
    print("Documentos de entrada:")
    for index, document in enumerate(DOCUMENTS):
        print(f"{index}. {document}")

    try:
        # Genera embeddings reales usando Sentence Transformers.
        embeddings = generate_document_embeddings(DOCUMENTS)
    except ImportError as exc:
        # Informa como instalar la dependencia faltante.
        print(str(exc))
        return

    print_section("Embeddings")
    print(f"Shape: {embeddings.shape}")

    l2_dist_manual = build_l2_distance_matrix(embeddings)
    l2_dist_manual_improved = build_l2_distance_matrix_improved(embeddings)
    print_section("L2 Distance")
    print_matrix("Manual", l2_dist_manual)
    print_matrix("Improved", l2_dist_manual_improved)
    print(
        "Manual equals improved:",
        np.allclose(l2_dist_manual, l2_dist_manual_improved, atol=NUMERICAL_TOLERANCE),
    )

    try:
        # Compara la implementacion manual contra Scipy.
        l2_dist_scipy = build_l2_distance_matrix_scipy(embeddings)
        print_matrix("Scipy", l2_dist_scipy)
        print(
            "Manual equals scipy:",
            np.allclose(l2_dist_manual, l2_dist_scipy, atol=NUMERICAL_TOLERANCE),
        )
    except ImportError as exc:
        # Permite ejecutar el spike aunque Scipy no exista aun.
        print(str(exc))

    dot_product_manual = build_dot_product_matrix(embeddings)
    dot_product_operator = build_dot_product_matrix_operator(embeddings)
    dot_product_distance = build_dot_product_distance_matrix(dot_product_manual)
    print_section("Dot Product")
    print_matrix("Manual", dot_product_manual)
    print_matrix("Operator", dot_product_operator)
    print_matrix("Distance", dot_product_distance)
    print(
        "Manual equals operator:",
        np.allclose(
            dot_product_manual,
            dot_product_operator,
            atol=NUMERICAL_TOLERANCE,
        ),
    )

    normalized_embeddings_manual = normalize_embeddings_manual(embeddings)
    normalized_lengths = verify_normalized_embeddings(normalized_embeddings_manual)
    cosine_similarity_manual = build_cosine_similarity_matrix(normalized_embeddings_manual)
    cosine_similarity_operator = build_cosine_similarity_matrix_operator(
        normalized_embeddings_manual
    )
    cosine_distance = build_cosine_distance_matrix(cosine_similarity_manual)
    print_section("Cosine Similarity")
    print(f"Normas normalizadas: {np.round(normalized_lengths, 6)}")
    print_matrix("Manual", cosine_similarity_manual)
    print_matrix("Operator", cosine_similarity_operator)
    print_matrix("Distance", cosine_distance)
    print(
        "Manual equals operator:",
        np.allclose(
            cosine_similarity_manual,
            cosine_similarity_operator,
            atol=NUMERICAL_TOLERANCE,
        ),
    )

    try:
        # Compara la normalizacion manual contra Torch.
        normalized_embeddings_from_torch = normalize_embeddings_torch(embeddings)
        print(
            "Manual equals torch:",
            np.allclose(
                normalized_embeddings_manual,
                normalized_embeddings_from_torch,
                atol=NUMERICAL_TOLERANCE,
            ),
        )
    except ImportError as exc:
        # Permite seguir si Torch aun no esta instalado.
        print(str(exc))

    query_result = search_documents_by_query(
        QUERY_TEXT,
        DOCUMENTS,
        normalized_embeddings_manual,
    )
    print_section("Query Search")
    print(f"Query: {QUERY_TEXT}")
    print(
        "Cosine scores:",
        np.round(query_result["similarity_scores"], 4),
    )
    print(f"Best match index: {query_result['best_match_index']}")
    print(f"Best match document: {query_result['best_match_document']}")
