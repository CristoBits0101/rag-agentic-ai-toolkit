# --- DEPENDENCIAS ---
from config.faiss_similarity_config import GRAPHICS_QUERY
from config.faiss_similarity_config import MEDICAL_QUERY
from config.faiss_similarity_config import PRIMARY_QUERY
from config.faiss_similarity_config import SAMPLE_INDEX
from config.faiss_similarity_config import SEMANTIC_QUERY
from config.faiss_similarity_config import SPACE_QUERY
from orchestration.faiss_index_orchestration import build_semantic_faiss_lab_context
from orchestration.faiss_preprocessing_orchestration import preprocess_text
from orchestration.faiss_search_orchestration import search_semantic_posts

# --- RUNNER ---
def print_section(title: str):
    # Separa visualmente cada seccion del laboratorio.
    print(f"\n=== {title} ===")


def print_results(query: str):
    # Imprime resultados procesados y originales para una consulta.
    print(f"Query: {query}")
    for result in search_semantic_posts(query):
        print(
            f"Rank {result['rank']} | distance: {result['distance']:.4f} | "
            f"category: {result['category']} | title: {result['title']}"
        )
        print(f"Processed: {result['processed_text'][:160]}")
        print(f"Original: {result['raw_text'][:160]}")
        print()


def run_semantic_similarity_faiss_lab():
    # Ejecuta la practica completa de semantic similarity con FAISS.
    context = build_semantic_faiss_lab_context()
    sample_post = context.raw_posts[SAMPLE_INDEX]["text"]

    print("Practica 11 Semantic Similarity With FAISS")

    print_section("Dataset")
    print(f"Posts cargados: {len(context.raw_posts)}")
    print("Categorias disponibles: motorcycles space graphics medicine")
    for index, post in enumerate(context.raw_posts[:3], start=1):
        print(f"\nSample post {index}:")
        print(post["text"])

    print_section("Preprocessing")
    print("Original post:")
    print(sample_post)
    print("\nPreprocessed post:")
    print(preprocess_text(sample_post))

    print_section("Vectorization And Indexing")
    print(f"Embedding shape: {context.embeddings.shape}")
    print(f"FAISS dimension: {context.embeddings.shape[1]}")
    print(f"FAISS indexed vectors: {context.index.ntotal}")

    print_section("FAISS Search")
    print_results(PRIMARY_QUERY)

    print_section("Semantic Search")
    print_results(SEMANTIC_QUERY)
    print_results(SPACE_QUERY)
    print_results(GRAPHICS_QUERY)
    print_results(MEDICAL_QUERY)
