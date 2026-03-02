# --- DEPENDENCIAS ---

# Sirve para definir las rutas de la API. 
from fastapi import APIRouter

# Importamos los routers de cada endpoint para luego incluirlos en el router principal.
from app.api.v1.endpoints.agents import router as agents_router
from app.api.v1.endpoints.chat import router as chat_router
from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.llm import router as llm_router
from app.api.v1.endpoints.prompts import router as prompts_router
from app.api.v1.endpoints.retrieval import router as retrieval_router

# --- PREFIJO DE RUTAS ---

# Definimos el prefijo para todas las rutas de esta versión.
router = APIRouter(prefix="/api/v1", tags=["API v1"])

# --- RUTAS DE LOS ENDPOINTS ---

# Concatenamos las rutas de cada endpoint al router principal. 
router.include_router(health_router)
router.include_router(agents_router)
router.include_router(chat_router)
router.include_router(llm_router)
router.include_router(retrieval_router)
router.include_router(prompts_router)
