from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from app.services.compression_service import CompressionService

router = APIRouter()

# Schema Pydantic untuk validasi item riwayat perjalanan
class TripItem(BaseModel):
    item_name: str
    category: str
    description: str

# Schema Pydantic untuk validasi input data riwayat perjalanan pengguna
class UserHistoryRequest(BaseModel):
    user_id: str
    raw_trips: List[Dict[str, Any]]  # Berisi daftar riwayat perjalanan mentah

@router.post("/compress-history", summary="Eksekusi Hierarchical Patch Compression")
async def compress_user_history(payload: UserHistoryRequest):
    """
    Endpoint untuk memproses riwayat perjalanan panjang pengguna 
    menjadi User Preference Profile melalui level kompresi hirarkis.
    """
    try:
        # Inisialisasi service compression
        compressor = CompressionService()
        
        # Eksekusi logika hirarki kompresi
        preference_profile = compressor.hierarchical_compress(payload.raw_trips)
        
        return {
            "status": "success",
            "message": "Riwayat perjalanan berhasil dikompresi secara hierarkis.",
            "user_id": payload.user_id,
            "preference_profile": preference_profile
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))