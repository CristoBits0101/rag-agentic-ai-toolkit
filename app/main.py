# --- DEPENDENCIAS ---


# Importa la clase principal de FastAPI.
from fastapi import FastAPI

# Importa la herramienta para gestionar configuración.
from pydantic_settings import BaseSettings, SettingsConfigDict

# Importa el router de la API v1 para incluirlo en la aplicación.
from app.api.v1.router import router as api_v1_router

# --- CONFIGURACIÓN ---


# Definir un modelo de configuración.
class Settings(BaseSettings):
    # Nombre de la aplicación para la documentación de FastAPI.
    app_author: str = "Cristo Suárez"
    app_description: str = (
        "A toolkit for building Retrieval-Augmented Generation (RAG) and Agentic AI applications."
    )
    app_name: str = "RAG and Agentic AI Toolkit"
    app_version: str = "1.0.0"
    # Configuración para cargar variables de entorno desde un archivo .env
    model_config = SettingsConfigDict(env_file=".env")


# Crea una instancia de la configuración.
settings = Settings()

# Crea una instancia de la aplicación FastAPI utilizando el nombre definido en la configuración.
app = FastAPI(
    description=settings.app_description,
    title=settings.app_name,
    version=settings.app_version,
    contact={"name": settings.app_author},
)


# --- RUTAS ---


# Ruta raíz para verificar que la aplicación está funcionando y para mostrar el nombre del servicio.
@app.get("/", tags=["Root"])
async def root():
    return {
        "author": settings.app_author,
        "service": settings.app_name,
        "description": settings.app_description,
        "version": settings.app_version,
    }


# Ruta útil para verificar la salud del servicio al monitoreo y despliegue.
@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}


# Incluye el router de la API v1 en la aplicación principal.
app.include_router(api_v1_router)
