# --- DEPENDENCIAS ---
# 1. Datos locales: Este archivo solo define documentos y ejemplos.

# --- DATOS ---
# 1. Documentos: Contenido usado por la demo de colecciones y filtros.
DEMO_ITEMS = [
    {
        "id": "doc_1",
        "document": "Polar bears live in Arctic sea ice and hunt seals.",
        "metadata": {"topic": "animals", "source": "wildlife.org", "version": 1.0},
    },
    {
        "id": "doc_2",
        "document": "pandas eat bamboo and spend much of the day foraging.",
        "metadata": {"topic": "animals", "source": "zoo.org", "version": 1.1},
    },
    {
        "id": "doc_3",
        "document": "LangChain is a Python framework for retrieval and agent workflows.",
        "metadata": {"topic": "tech", "source": "langchain.com", "version": 0.2},
    },
    {
        "id": "doc_4",
        "document": "LlamaIndex helps organize documents for RAG and vector search.",
        "metadata": {"topic": "tech", "source": "llamaindex.ai", "version": 0.2},
    },
    {
        "id": "doc_5",
        "document": "Fleet routing systems combine maps GPS and live traffic updates.",
        "metadata": {"topic": "geo", "source": "maps.example", "version": 1.0},
    },
    {
        "id": "doc_6",
        "document": "ChromaDB supports metadata filtering vector search and document search.",
        "metadata": {"topic": "tech", "source": "chromadb.dev", "version": 1.0},
    },
]
BASIC_QUERY_TEXT = "Which document talks about polar bears and Arctic wildlife?"
TECH_QUERY_TEXT = "Which technical document focuses on Python retrieval workflows?"
RAG_QUERY_TEXT = "How does RAG use vector databases to retrieve context for a query?"
RECOMMENDATION_QUERY_TEXT = (
    "How can vector databases recommend similar products and content?"
)
CASE_SENSITIVE_TEXT = "Pandas"
CASE_SENSITIVE_TEXT_EXPECTED = "pandas"
METADATA_FILTER = {"topic": "animals"}
COMPLEX_METADATA_FILTER = {
    "$and": [
        {"source": {"$in": ["langchain.com", "llamaindex.ai"]}},
        {"version": {"$lt": 0.3}},
    ]
}
DOCUMENT_FILTER = {"$contains": "pandas"}
DOCUMENT_FILTER_NEGATIVE = {"$not_contains": "library"}
CRUD_DEMO_ITEM = {
    "id": "doc_99",
    "document": (
        "Recommendation systems use vector databases to suggest similar products and content."
    ),
    "metadata": {"topic": "recommendation", "source": "product.blog", "version": 1.0},
}
