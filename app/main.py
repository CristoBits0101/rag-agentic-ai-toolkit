# Importar el framework FastAPI
from fastapi import FastAPI

# Importar BaseSettings de pydantic_settings para manejar la configuración de la aplicación
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AI Agents Dev"

    class Config:
        env_file = ".env"


settings = Settings()

app = FastAPI(title=settings.app_name)


@app.get("/health")
async def health():
    return {"status": "dev running"}
