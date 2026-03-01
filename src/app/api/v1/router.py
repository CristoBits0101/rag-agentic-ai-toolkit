from fastapi import APIRouter

from .agent_router import router as agent_router
from .chat_router import router as chat_router
from .llm_router import router as llm_router
from .prompt_router import router as prompt_router
from .rag_router import router as rag_router

router = APIRouter(prefix="/api/v1", tags=["API v1"])

router.include_router(agent_router)
router.include_router(chat_router)
router.include_router(llm_router)
router.include_router(prompt_router)
router.include_router(rag_router)
