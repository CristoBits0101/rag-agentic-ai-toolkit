from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["Health v1"])


@router.get("/")
async def health_v1() -> dict[str, str]:
    return {"status": "ok"}
