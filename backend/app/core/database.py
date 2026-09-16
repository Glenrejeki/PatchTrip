import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Mengambil URL database dari environment variables atau file config
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:password123@db:5432/patchtrip_db"
)

# Membuat SQLAlchemy Engine untuk menghubungkan FastAPI ke PostgreSQL
engine = create_engine(DATABASE_URL)

# Membuat SessionLocal untuk mengelola sesi transaksi database per request
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class yang akan diwarisi oleh model-model tabel database (SQLAlchemy Models)
Base = declarative_base()

def get_db():
    """
    Fungsi Dependency Injection FastAPI untuk membuka dan menutup 
    koneksi/sesi database secara otomatis pada setiap HTTP Request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()