from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from app.db.session import SessionLocal
from app.models.transport_model import TransportRouteModel, TransportScheduleModel

def run_transport_scraper_job():
    """
    Background worker dinamis murni (APScheduler) untuk mengambil data jadwal 
    secara otomatis tanpa data dummy atau seeder statis di dalam kode.
    """
    print(f"[{datetime.now()}] Background Scheduler: Memulai sinkronisasi jadwal transportasi...")
    
    db = SessionLocal()
    try:
        # PENGINGAT: Di sinilah tempat Anda meletakkan logika pemanggilan API publik / scraper 
        # murni secara legal untuk tesis Anda. 
        fresh_transport_data = [] # Dikosongkan secara default agar bersih dari data palsu
        
        if not fresh_transport_data:
            print("Background Scheduler: Belum ada data baru yang ditarik dari sumber eksternal.")
            return

        for item in fresh_transport_data:
            route = db.query(TransportRouteModel).filter_by(
                origin_city=item["origin_city"],
                destination_city=item["destination_city"],
                provider_name=item["provider_name"]
            ).first()

            if not route:
                route = TransportRouteModel(
                    transport_type=item["transport_type"],
                    provider_name=item["provider_name"],
                    origin_city=item["origin_city"],
                    destination_city=item["destination_city"],
                    base_price=item["base_price"]
                )
                db.add(route)
                db.commit()
                db.refresh(route)

            schedule = TransportScheduleModel(
                route_id=route.id,
                departure_time=item["departure_time"],
                arrival_time=item["arrival_time"],
                status="AVAILABLE"
            )
            db.add(schedule)
            db.commit()

        print("Background Scheduler: Sinkronisasi data ke PostgreSQL berhasil diperbarui!")

    except Exception as e:
        print(f"Error pada Background Scheduler: {e}")
        db.rollback()
    finally:
        db.close()

# Inisialisasi APScheduler
scheduler = BackgroundScheduler()
# Menjadwalkan tugas berjalan otomatis setiap 24 jam sekali di latar belakang
scheduler.add_job(run_transport_scraper_job, 'interval', hours=24)