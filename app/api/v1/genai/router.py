# --- DEPENDENCIAS ---
from fastapi import APIRouter

router = APIRouter(
    prefix="/genai",
    tags=["GenAI"],
)


@router.get("/")
async def genai():
    return{"genai": "GenAI app built successfully!"}