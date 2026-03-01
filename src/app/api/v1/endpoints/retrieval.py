from fastapi import APIRouter

router = APIRouter(prefix="/rag", tags=["RAG"])


@router.get("/")
async def rag() -> dict[str, str]:
    return {"rag": "Document summarized successfully!"}
