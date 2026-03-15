from fastapi import APIRouter

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.get("/")
async def chat() -> dict[str, str]:
    return {"chat": "Chat app generated successfully!"}
