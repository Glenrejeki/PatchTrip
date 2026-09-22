from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter(prefix="/transport", tags=["Transport Management"])

# Skema Pydantic sementara di dalam endpoint untuk memastikan tidak ada error import session database eksternal
class TransportScheduleResponse(BaseModel):
    id: int
    departure_time: datetime
    arrival_time: datetime
    status: str

    model_config = {"from_attributes": True}

class TransportRouteResponse(BaseModel):
    id: int
    transport_type: str
    provider_name: str
    origin_city: str
    destination_city: str
    base_price: Optional[float] = None
    schedules: List[TransportScheduleResponse] = []

    model_config = {"from_attributes": True}

@router.get("/search", response_model=List[TransportRouteResponse])
def search_transport_schedules(
    origin: str = Query(..., description="Kota asal keberangkatan, contoh: Jakarta"),
    destination: str = Query(..., description="Kota tujuan, contoh: Yogyakarta")
):
    """
    Endpoint untuk mencari informasi rute dan jadwal transportasi.
    """
    # Karena tabel di DBeaver baru saja disiapkan, kita kembalikan list kosong yang aman 
    # tanpa error impor database hingga sesi engine SQLAlchemy utama Anda dipetakan.
    return []