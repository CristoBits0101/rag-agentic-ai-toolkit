# --- DEPENDENCIAS ---
from fastapi import APIRouter
from .rag_document_summarization_langchain_llms import summarize_document

router = APIRouter(
    prefix="/rag",
    tags=["RAG"],
)


@router.get("/")
async def rag():
    return {"rag": "Document summarized successfully!"}
