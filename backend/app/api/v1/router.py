from fastapi import APIRouter
from app.api.v1.endpoints import compression, retrieval, generator
# Import service OSM & OSRM yang sudah dibuat sebelumnya
from app.services.osm_service import fetch_pois_from_osm, get_city_coordinates
from app.services.osrm_service import get_travel_time_matrix
# Import endpoint transport baru untuk menangani rute & jadwal transportasi secara dinamis
from app.api.v1.endpoints.transport import router as transport_router

# Inisialisasi APIRouter utama untuk API version 1
api_router = APIRouter()

# Menghubungkan endpoint kompresi hierarkis (Hierarchical Patch Compression)
api_router.include_router(
    compression.router, 
    prefix="/compression", 
    tags=["Hierarchical Patch Compression"]
)

# Menghubungkan endpoint semantic dense retrieval (BGE-M3 & FAISS)
api_router.include_router(
    retrieval.router, 
    prefix="/retrieval", 
    tags=["Semantic Dense Retrieval"]
)

# Menghubungkan endpoint RAG & generasi itinerary LLM (Qwen3-8B)
api_router.include_router(
    generator.router, 
    prefix="/generator", 
    tags=["RAG & Itinerary Generation"]
)

# ==========================================
# ENDPOINT MODUL TRANSPORTASI (Database Caching / PostgreSQL)
# ==========================================

# Menghubungkan endpoint manajemen rute dan jadwal transportasi antarkota
api_router.include_router(
    transport_router, 
    prefix="", 
    tags=["Transport Management"]
)

# ==========================================
# ENDPOINT TAMBAHAN: Real-Time Indonesia Data (OSM & OSRM)
# ==========================================

@api_router.get("/explore/{city}", tags=["Real-Time Indonesia Data"])
def explore_city(city: str):
    """Endpoint untuk mengetes pengambilan data POI real-time dari OpenStreetMap"""
    pois = fetch_pois_from_osm(city)
    lat, lon = get_city_coordinates(city)
    
    return {
        "status": "success",
        "city": city,
        "coordinates": {"lat": lat, "lon": lon},
        "total_pois_found": len(pois),
        "data": pois[:15] # Menampilkan 15 data teratas sebagai sampel respons
    }

@api_router.get("/route-check", tags=["Real-Time Indonesia Data"])
def route_check(lat1: float, lon1: float, lat2: float, lon2: float):
    """Endpoint untuk mengetes kalkulasi jarak dan waktu tempuh rute via OSRM"""
    dist_km, duration_mins = get_travel_time_matrix(lat1, lon1, lat2, lon2)
    return {
        "status": "success",
        "distance_km": dist_km,
        "estimated_duration_minutes": duration_mins
    }