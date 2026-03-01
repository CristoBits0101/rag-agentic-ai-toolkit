# --- DEPENDENCIAS ---

# Clase principal para crear la instancia de la aplicación FastAPI.
from fastapi import FastAPI

# Router que agrupa y registra todos los endpoints de la versión v1 de la API.
from app.api.v1.router import router as api_v1_router

# Instancia la configuración cargada desde las variables de entorno.
from app.core.settings import settings

# --- CONFIGURACIÓN DE LA APLICACIÓN ---

# Crea la instancia de la aplicación FastAPI con la configuración proporcionada.
app = FastAPI(
    # Título de la aplicación mostrado en la documentación automática.
    title=settings.app_name,
    # Descripción de la aplicación mostrada en la documentación automática.
    description=settings.app_description,
    # Versión de la aplicación mostrada en la documentación automática.
    version=settings.app_version,
)

# --- ENDPOINTS DE PRUEBA ---

# Endpoint para verificar la salud de la aplicación útil para monitoreo y despliegue.
@app.get("/health", tags=["Health"])
async def health_check() -> dict[str, str]:
    return {"status": "ok"}

# Incluye todos los endpoints definidos en el router de la carpeta api/v1.
app.include_router(api_v1_router)
