from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router

# Import scheduler dan task background yang sudah kita buat
from app.core.scheduler import scheduler, run_transport_scraper_job

app = FastAPI(title="PatchTrip AI Backend", version="1.0.0")

# Konfigurasi CORS agar frontend dapat mengakses API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Event Lifecycle: Dijalankan otomatis saat FastAPI mulai menyala
@app.on_event("startup")
def startup_event():
    # Menyalakan background scheduler otomatis di dalam memori
    scheduler.start()
    print("Background Scheduler (APScheduler) berhasil diaktifkan!")
    
    # (Opsional) Jika ingin langsung mengetes tugas scraping saat server pertama kali dinyalakan:
    # run_transport_scraper_job()

# Event Lifecycle: Dijalankan otomatis saat FastAPI dimatikan
@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()
    print("Background Scheduler dimatikan.")

# Menghubungkan router utama API v1
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "PatchTrip Backend is running!"}