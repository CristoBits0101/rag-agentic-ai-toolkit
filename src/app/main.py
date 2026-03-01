from fastapi import FastAPI

from app.api.v1.router import router as api_v1_router
from app.core.settings import settings

app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    contact={"name": settings.app_author},
)


@app.get("/", tags=["Root"])
async def root() -> dict[str, str]:
    return {
        "author": settings.app_author,
        "service": settings.app_name,
        "description": settings.app_description,
        "version": settings.app_version,
    }


@app.get("/health", tags=["Health"])
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(api_v1_router)
