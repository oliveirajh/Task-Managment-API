from pydantic_settings import BaseSettings
from typing import List
import os
from pathlib import Path

# Caminho para a raiz do projeto
BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./tasks.db"

    # App Info
    VERSION: str = "0.1.0"
    PROJECT_NAME: str = "My FastAPI Project"
    API_V1_STR: str = "/api/v1"

    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    DEBUG: bool = True

    class Config:
        env_file = BASE_DIR / ".env"  # ✅ Busca .env na raiz
        env_file_encoding = "utf-8"

settings = Settings()

