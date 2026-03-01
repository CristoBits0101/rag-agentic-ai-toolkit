# --- DEPENDENCIAS ---
from fastapi import APIRouter

router = APIRouter(
    prefix="/agent",
    tags=["Agent"],
)


@router.get("/")
async def agent():
    return {"agent": "Agent app built successfully!"}
