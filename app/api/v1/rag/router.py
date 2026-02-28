# --- DEPENDENCIAS ---
from fastapi import APIRouter

router = APIRouter(
    prefix="/rag",
    tags=["RAG"],
)


@router.get("/")
async def rag():
    return {"rag": "Document summarized successfully!"}
