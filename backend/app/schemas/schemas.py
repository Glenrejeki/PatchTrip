from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

# ==========================================
# 1. SCHEMA UNTUK ENTITAS USER & DATABASE
# ==========================================

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # Kompatibilitas dengan SQLAlchemy model (Pydantic v2)


# ==========================================
# 2. SCHEMA UNTUK POINT OF INTEREST (POI)
# ==========================================

class POIResponse(BaseModel):
    id: int
    name: str
    category: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    similarity_score: Optional[float] = None  # Skor kedekatan dari semantic retrieval

    class Config:
        from_attributes = True


# ==========================================
# 3. SCHEMA UNTUK RIWAYAT PERJALANAN
# ==========================================

class TravelHistoryCreate(BaseModel):
    trip_name: str
    visit_date: Optional[datetime] = None
    details: Optional[str] = None

class TravelHistoryResponse(TravelHistoryCreate):
    id: int
    user_id: int

    class Config:
        from_attributes = True


# ==========================================
# 4. SCHEMA UNTUK MODUL HIERARCHICAL COMPRESSION
# ==========================================

class CompressionRequest(BaseModel):
    user_id: str
    raw_trips: List[Dict[str, Any]] = Field(
        ..., 
        description="Daftar riwayat perjalanan mentah pengguna untuk diproses 3-level patch compression"
    )

class CompressionResponse(BaseModel):
    status: str
    message: str
    user_id: str
    preference_profile: str  # Hasil akhir User Preference Profile (Level 3)


# ==========================================
# 5. SCHEMA UNTUK MODUL SEMANTIC RETRIEVAL
# ==========================================

class RetrievalRequest(BaseModel):
    user_preference_profile: str = Field(
        ..., 
        description="Profil preferensi implisit hasil kompresi hierarkis"
    )
    top_k: int = Field(5, description="Jumlah kandidat destinasi POI teratas yang ingin diambil")

class RetrievalResponse(BaseModel):
    status: str
    message: str
    query_profile: str
    total_retrieved: int
    candidates: List[POIResponse]


# ==========================================
# 6. SCHEMA UNTUK MODUL RAG & GENERATOR
# ==========================================

class GenerationRequest(BaseModel):
    user_preference_profile: str
    retrieved_pois: List[Dict[str, Any]]
    constraints: Dict[str, Any] = Field(
        ..., 
        description="Batasan perjalanan seperti budget, durasi_hari, dan lokasi tujuan"
    )

class GenerationResponse(BaseModel):
    status: str
    message: str
    itinerary: str  # Teks lengkap hasil akhir rekomendasi itinerary dari Qwen3-8B[cite: 1, 3]