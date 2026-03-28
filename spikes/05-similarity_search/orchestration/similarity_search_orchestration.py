# --- DEPENDENCIAS ---
# 1. Numpy: Para algebra matricial y seleccion del mayor coseno.
# 2. Configuracion: Para usar el modelo de embeddings por defecto.
# 3. Gateway: Para generar embeddings de documentos y consultas.
# 4. Metricas: Para normalizar embeddings antes de comparar.
import numpy as np

from config.similarity_runtime_config import MODEL_NAME
from models.similarity_embedding_gateway import encode_texts
from orchestration.similarity_metrics_orchestration import normalize_embeddings_manual

# --- SEARCH ---
# 1.1. Funcion para generar embeddings de documentos.
def generate_document_embeddings(
    documents: list[str],
    model_name: str = MODEL_NAME,
) -> np.ndarray:
    # Convierte los documentos en embeddings listos para comparar.
    return np.asarray(encode_texts(documents, model_name=model_name))


# 1.2. Funcion para generar embedding de una consulta.
def generate_query_embedding(
    query_text: str,
    model_name: str = MODEL_NAME,
) -> np.ndarray:
    # Convierte la consulta en un solo embedding de dos dimensiones.
    return np.asarray(encode_texts([query_text], model_name=model_name))


# 1.3. Funcion para calcular similitud coseno entre documentos y consulta.
def build_query_cosine_similarity(
    normalized_document_embeddings: np.ndarray,
    normalized_query_embedding: np.ndarray,
) -> np.ndarray:
    # Devuelve una columna con la similitud de cada documento frente a la consulta.
    return normalized_document_embeddings @ normalized_query_embedding.T


# 1.4. Funcion para obtener la posicion del documento mas similar.
def find_best_match_index(similarity_scores: np.ndarray) -> int:
    # Devuelve el indice con la similitud mas alta.
    return int(similarity_scores.argmax())


# 1.5. Funcion para buscar el mejor documento usando un embedding de consulta.
def search_with_query_embedding(
    documents: list[str],
    normalized_document_embeddings: np.ndarray,
    normalized_query_embedding: np.ndarray,
) -> dict:
    # Calcula las similitudes frente a la consulta.
    similarity_scores = build_query_cosine_similarity(
        normalized_document_embeddings,
        normalized_query_embedding,
    )
    best_match_index = find_best_match_index(similarity_scores)

    # Devuelve el resultado principal del retrieval.
    return {
        "best_match_index": best_match_index,
        "best_match_document": documents[best_match_index],
        "similarity_scores": similarity_scores.reshape(-1),
    }


# 1.6. Funcion para buscar el documento mas similar desde texto natural.
def search_documents_by_query(
    query_text: str,
    documents: list[str],
    normalized_document_embeddings: np.ndarray,
    model_name: str = MODEL_NAME,
) -> dict:
    # Genera el embedding de la consulta y lo normaliza.
    query_embedding = generate_query_embedding(query_text, model_name=model_name)
    normalized_query_embedding = normalize_embeddings_manual(query_embedding)

    # Reutiliza la funcion de busqueda basada en embeddings.
    return search_with_query_embedding(
        documents,
        normalized_document_embeddings,
        normalized_query_embedding,
    )
