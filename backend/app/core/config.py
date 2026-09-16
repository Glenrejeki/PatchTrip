import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Konfigurasi Dasar Aplikasi
    APP_NAME: str = "PatchTrip"
    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"

    # Konfigurasi Koneksi Database PostgreSQL
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql://postgres:password123@db:5432/patchtrip_db"
    )

    # Konfigurasi AI Models & Vector Store
    EMBEDDING_MODEL_PATH: str = os.getenv("EMBEDDING_MODEL_PATH", "BAAI/bge-m3")
    VECTOR_STORE_PATH: str = os.getenv("VECTOR_STORE_PATH", "backend/data/vector_store")
    LLM_MODEL_NAME: str = os.getenv("LLM_MODEL_NAME", "Qwen/Qwen2.5-7B-Instruct")

    class Config:
        env_file = ".env"
        case_sensitive = True

# Instansiasi objek settings agar bisa dipanggil di modul lain
settings = Settings()