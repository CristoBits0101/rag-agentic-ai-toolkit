# --- DEPENDENCIAS ---


# Importa la clase principal de FastAPI.
from fastapi import FastAPI

# Importa la herramienta para gestionar configuración.
from pydantic_settings import BaseSettings, SettingsConfigDict

# Importa el router de la API v1 para incluirlo en la aplicación.
from app.api.v1.router import router as api_v1_router


# --- CONFIGURACIÓN ---


# Clase para definir un modelo de configuración.
class Settings(BaseSettings):
    # Autor de la aplicación útil para la documentación y el contacto en la API.
    app_author: str = "Cristo Suárez"
    # Descripción de la aplicación para la documentación de FastAPI útil para que los usuarios entiendan el propósito del servicio.
    app_description: str = (
        "A toolkit for building Retrieval-Augmented Generation (RAG) and Agentic AI applications."
    )
    # Nombre de la aplicación para la documentación de FastAPI útil para identificar el servicio en la documentación y en los logs.
    app_name: str = "RAG and Agentic AI Toolkit"
    # Versión de la aplicación para la documentación de FastAPI útil para el versionado y la gestión de cambios en la API.
    app_version: str = "1.0.0"
    # Configura la clase para que lea las variables de entorno desde un archivo .env en el directorio raíz del proyecto.
    # Esto permite gestionar la configuración de manera más segura y flexible especialmente para despliegues en producción.
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
