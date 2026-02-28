# --- DEPENDENCIAS ---
from fastapi import APIRouter

router = APIRouter(
    prefix="/llm",
    tags=["LLM"],
)


@router.get("/")
async def llm():
    return {"llm": "LLM app generated successfully!"}
