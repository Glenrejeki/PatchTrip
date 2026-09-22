from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class TransportScheduleResponse(BaseModel):
    id: int
    departure_time: datetime
    arrival_time: datetime
    status: str

    # Konfigurasi agar model Pydantic bisa membaca objek SQLAlchemy secara langsung
    model_config = ConfigDict(from_attributes=True)


class TransportRouteResponse(BaseModel):
    id: int
    transport_type: str
    provider_name: str
    origin_city: str
    destination_city: str
    base_price: Optional[float] = None
    schedules: list[TransportScheduleResponse] = []

    model_config = ConfigDict(from_attributes=True)