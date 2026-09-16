from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from app.services.rag_service import RAGService

router = APIRouter()

# Schema Pydantic untuk validasi input data generasi itinerary
class GenerationRequest(BaseModel):
    user_preference_profile: str     # Profil implisit hasil kompresi hierarkis
    retrieved_pois: List[Dict[str, Any]] # Kandidat POI hasil semantic retrieval
    constraints: Dict[str, Any]      # Batasan perjalanan (misal: budget, durasi_hari, lokasi)

@router.post("/generate-itinerary", summary="Eksekusi RAG & LLM Generation Itinerary")
async def generate_itinerary(payload: GenerationRequest):
    """
    Endpoint untuk menghasilkan rekomendasi itinerary wisata personal 
    menggunakan LangChain dan Qwen3-8B berdasarkan profil dan kandidat POI.
    """
    try:
        # Inisialisasi service RAG
        rag_engine = RAGService()
        
        # Eksekusi proses generasi teks itinerary
        itinerary_result = rag_engine.generate_itinerary(
            user_profile=payload.user_preference_profile,
            pois=payload.retrieved_pois,
            constraints=payload.constraints
        )
        
        return {
            "status": "success",
            "message": "Itinerary berhasil di-generate secara personal dan rasional.",
            "itinerary": itinerary_result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))