from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router
from app.core.config import settings
from app.utils.logger import logger

# Inisialisasi aplikasi FastAPI dengan metadata dari konfigurasi
app = FastAPI(
    title=settings.APP_NAME,
    description="Backend API untuk sistem perencana perjalanan berbasis AI (PatchTrip)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Konfigurasi Middleware CORS (Cross-Origin Resource Sharing) untuk koneksi ke Frontend Next.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Batasi domain asal di lingkungan production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mendaftarkan API Router utama versi 1 (v1)
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.on_event("startup")
async def startup_event():
    """Event yang dijalankan saat server FastAPI pertama kali menyala."""
    logger.info(f"=== Aplikasi {settings.APP_NAME} Berhasil Dinyalakan ===")
    logger.info(f"Dokumentasi API Swagger aktif di: /docs")

@app.get("/", summary="Health Check Endpoint")
async def root_health_check():
    """Endpoint pengecekan status server backend."""
    return {
        "status": "online",
        "app_name": settings.APP_NAME,
        "message": "Sistem Backend PatchTrip siap digunakan."
    }