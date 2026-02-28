# --- DEPENDENCIAS ---


# Importa la clase principal de FastAPI.
from fastapi import FastAPI

# Importa la herramienta para gestionar configuración.
from pydantic_settings import BaseSettings, SettingsConfigDict


# --- CONFIGURACIÓN ---


# Definir un modelo de configuración.
class Settings(BaseSettings):
    # Nombre de la aplicación para la documentación de FastAPI.
    app_name: str = "RAG and Agentic AI Toolkit"
    # Configuración para cargar variables de entorno desde un archivo .env
    model_config = SettingsConfigDict(env_file=".env")


# Crea una instancia de la configuración.
settings = Settings()

# Crea una instancia de la aplicación FastAPI utilizando el nombre definido en la configuración.
app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
)


# --- RUTAS ---


# Ruta raíz para verificar que la aplicación está funcionando y para mostrar el nombre del servicio.
@app.get("/", tags=["Root"])
async def root():
    return {"service": settings.app_name}


# Ruta útil para verificar la salud del servicio al monitoreo y despliegue.
@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}
