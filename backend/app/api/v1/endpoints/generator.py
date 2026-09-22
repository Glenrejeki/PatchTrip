from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
from app.services.rag_service import rag_engine
import psycopg2
import json

router = APIRouter()

# Skema Request untuk Generate Itinerary
class ItineraryRequest(BaseModel):
    destination: str
    duration: int
    budget: str
    preferences: str
    user_id: Optional[str] = "user_thesis_123"

# Skema Request untuk Menyimpan Itinerary ke Database
class SaveItineraryRequest(BaseModel):
    user_id: str
    itinerary_content: Dict[str, Any]

@router.post("/generate")
def generate_itinerary(data: ItineraryRequest):
    # Gabungkan preferensi dan destinasi sebagai query pencarian RAG
    query = f"{data.destination} {data.preferences}"
    
    # Ambil rekomendasi POI relevan dari FAISS vector store
    retrieved_pois = rag_engine.retrieve_similar_pois(query, top_k=3)
    
    # Format hasil respons untuk ditampilkan di Frontend
    itinerary_output = f"=== HASIL GENERASI PATCHTRIP (RAG) ===\n"
    itinerary_output += f"Destinasi: {data.destination}\n"
    itinerary_output += f"Durasi: {data.duration} Hari | Budget: {data.budget}\n\n"
    
    itinerary_output += "[Rekomendasi Tempat Berdasarkan Preferensi Anda]:\n"
    for i, poi in enumerate(retrieved_pois, 1):
        itinerary_output += f"- {i}. {poi.get('name')} ({poi.get('city', 'Lokasi')})\n"
        itinerary_output += f"  Deskripsi: {poi.get('description')}\n\n"
        
    itinerary_output += "Status: Itinerary berhasil disusun secara nyata menggunakan FAISS & Vector Embedding!"

    return {
        "status": "success",
        "destination": data.destination,
        "duration": data.duration,
        "budget": data.budget,
        "preferences": data.preferences,
        "itinerary": itinerary_output,
        "raw_pois": retrieved_pois
    }

@router.post("/save")
def save_itinerary(data: SaveItineraryRequest):
    try:
        # Koneksi ke database PostgreSQL lokal
        conn = psycopg2.connect(
            dbname="patchtrip_db",
            user="postgres",
            password="password123",
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()
        
        # Eksekusi penyimpanan data JSON ke tabel itineraries
        cur.execute(
            "INSERT INTO itineraries (user_id, itinerary_content) VALUES (%s, %s)",
            (data.user_id, json.dumps(data.itinerary_content))
        )
        
        conn.commit()
        cur.close()
        conn.close()
        
        print(f"[INFO] Sukses menyimpan itinerary untuk user: {data.user_id} ke PostgreSQL.")
        
        return {
            "status": "success",
            "message": "Itinerary berhasil disimpan ke database PostgreSQL",
            "user_id": data.user_id
        }
    except Exception as e:
        print(f"[ERROR DB SAVE]: {e}")
        raise HTTPException(status_code=500, detail=str(e))