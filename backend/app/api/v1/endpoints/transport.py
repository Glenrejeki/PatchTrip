from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.transport_model import TransportRouteModel, TransportScheduleModel
from app.schemas.transport_schema import TransportRouteResponse
from app.services.transport_fetcher import fetch_live_transport_data

router = APIRouter(prefix="/transport", tags=["Transport Management"])

@router.get("/search", response_model=List[TransportRouteResponse])
def search_transport_schedules(
    origin: str = Query(..., description="Kota asal, contoh: Jakarta"),
    destination: str = Query(..., description="Kota tujuan, contoh: Yogyakarta"),
    db: Session = Depends(get_db)
):
    """
    Endpoint pencarian rute: Membaca database lokal agar super cepat. 
    Jika kosong, otomatis menarik data real-time dan menyimpannya ke DB.
    """
    # 1. Cek ke database PostgreSQL lokal terlebih dahulu
    routes = db.query(TransportRouteModel).filter(
        TransportRouteModel.origin_city.ilike(f"%{origin}%"),
        TransportRouteModel.destination_city.ilike(f"%{destination}%")
    ).all()

    # 2. Jika data tidak ada di database lokal, ambil secara otomatis (Lazy Loading)
    if not routes:
        print(f"Data rute {origin} -> {destination} tidak ditemukan di lokal. Menarik data secara otomatis...")
        
        # Ambil data secara dinamis dari fungsi fetcher
        live_data = fetch_live_transport_data(origin, destination)
        
        if not live_data:
            raise HTTPException(
                status_code=404, 
                detail=f"Jadwal transportasi dari {origin} ke {destination} belum tersedia atau gagal ditarik dari sumber eksternal."
            )

        # Simpan otomatis ke PostgreSQL agar pencarian berikutnya instan
        for item in live_data:
            new_route = TransportRouteModel(
                transport_type=item["transport_type"],
                provider_name=item["provider_name"],
                origin_city=item["origin_city"],
                destination_city=item["destination_city"],
                base_price=item["base_price"]
            )
            db.add(new_route)
            db.commit()
            db.refresh(new_route)

            new_schedule = TransportScheduleModel(
                route_id=new_route.id,
                departure_time=item["departure_time"],
                arrival_time=item["arrival_time"],
                status="AVAILABLE"
            )
            db.add(new_schedule)
            db.commit()

        # Ambil ulang dari database lokal setelah berhasil disimpan otomatis
        routes = db.query(TransportRouteModel).filter(
            TransportRouteModel.origin_city.ilike(f"%{origin}%"),
            TransportRouteModel.destination_city.ilike(f"%{destination}%")
        ).all()

    return routes