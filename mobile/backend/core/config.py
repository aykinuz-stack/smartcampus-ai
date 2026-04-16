"""Backend ayarlari — .env'den cekilir."""
from __future__ import annotations

from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Ortak ayarlar."""

    # Uygulama
    APP_NAME: str = "SmartCampusAI Mobile Backend"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    API_PREFIX: str = "/api/v1"

    # CORS
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:8501",   # Streamlit
        "http://127.0.0.1:8501",
        "capacitor://localhost",    # Flutter WebView
        "http://localhost",
    ]

    # JWT
    JWT_SECRET_KEY: str = "change-me-in-production-32-char-random-string"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Veri yolu (Streamlit ile AYNI)
    DATA_DIR: Path = Path(__file__).resolve().parent.parent.parent.parent / "data"
    TENANT_DEFAULT: str = "default"

    # Rate limit
    RATE_LIMIT_PER_MIN: int = 100

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
