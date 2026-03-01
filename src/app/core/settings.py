from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_author: str = "Cristo Suarez"
    app_description: str = (
        "A toolkit for building Retrieval-Augmented Generation (RAG) and Agentic AI applications."
    )
    app_name: str = "RAG and Agentic AI Toolkit"
    app_version: str = "1.0.0"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
