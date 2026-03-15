# --- DEPENDENCIAS ---
from config.faiss_similarity_config import DEFAULT_TOP_K
from models.faiss_semantic_embedding_gateway import build_semantic_vector
from orchestration.faiss_index_orchestration import build_semantic_faiss_lab_context
from orchestration.faiss_preprocessing_orchestration import preprocess_text

# --- BUSQUEDA ---
def search_semantic_posts(query_text: str, top_k: int = DEFAULT_TOP_K) -> list[dict]:
    # Ejecuta busqueda por similitud sobre el indice FAISS.
    context = build_semantic_faiss_lab_context()
    processed_query = preprocess_text(query_text)
    query_vector = build_semantic_vector(processed_query).reshape(1, -1)
    distances, indices = context.index.search(query_vector, top_k)
    results = []

    for rank, index in enumerate(indices[0], start=1):
        results.append(
            {
                "rank": rank,
                "distance": float(distances[0][rank - 1]),
                "index": int(index),
                "category": context.raw_posts[index]["category"],
                "title": context.raw_posts[index]["title"],
                "processed_text": context.processed_documents[index],
                "raw_text": context.raw_posts[index]["text"],
            }
        )

    return results
