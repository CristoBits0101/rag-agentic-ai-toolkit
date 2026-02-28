# --- DEPENDENCIAS ---
from fastapi import APIRouter

router = APIRouter(
    prefix="/prompt",
    tags=["Prompt"],
)


@router.get("/")
async def prompt():
    return {"prompt": "Prompt generated successfully!"}
