# --- DEPENDENCIAS ---

from fastapi import APIRouter

# Importar los routers de cada módulo
from .genai.router import router as genai_router
from .gradio.router import router as gradio_router
from .llm.router import router as llm_router
from .prompt.router import router as prompt_router
from .rag.router import router as rag_router

# Prefijo común para todas las rutas de la API
router = APIRouter(prefix="/api/v1", tags=["API v1"])

router.include_router(genai_router)
router.include_router(gradio_router)
router.include_router(llm_router)
router.include_router(prompt_router)
router.include_router(rag_router)
