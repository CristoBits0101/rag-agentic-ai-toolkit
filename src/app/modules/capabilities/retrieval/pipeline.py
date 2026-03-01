from app.modules.capabilities.retrieval.retriever import retrieve


def run_pipeline(query: str) -> str:
    docs = retrieve(query)
    return "\n".join(docs)
