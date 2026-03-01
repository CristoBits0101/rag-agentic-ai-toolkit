from fastapi import APIRouter

from app.api.v1.endpoints.agents import router as agents_router
from app.api.v1.endpoints.chat import router as chat_router
from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.llm import router as llm_router
from app.api.v1.endpoints.prompts import router as prompts_router
from app.api.v1.endpoints.retrieval import router as retrieval_router

router = APIRouter(prefix="/api/v1", tags=["API v1"])

router.include_router(health_router)
router.include_router(agents_router)
router.include_router(chat_router)
router.include_router(llm_router)
router.include_router(retrieval_router)
router.include_router(prompts_router)
