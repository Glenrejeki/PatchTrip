import requests
from bs4 import BeautifulSoup
from datetime import datetime
from app.core.celery_app import celery_app
from app.db.session import SessionLocal  # Sesi database SQLAlchemy manual untuk background worker
from app.models.transport_model import TransportRouteModel, TransportScheduleModel

@celery_app.task(name="app.tasks.transport_task.run_transport_scraper")
def run_transport_scraper():
    """
    Fungsi latar belakang yang berjalan otomatis (tanpa intervensi pengguna).
    Melakukan scraping data nyata, lalu menyimpannya ke PostgreSQL.
    """
    print("Background Worker: Memulai proses scraping jadwal transportasi...")
    
    # Buka sesi database mandiri untuk background task
    db = SessionLocal()
    try:
        # CONTOH IMPLEMENTASI SCRAPING NYATA:
        # Misalkan kita menargetkan situs jadwal publik atau API terbuka.
        # (Ganti URL di bawah dengan target situs web nyata yang ingin Anda scrape)
        target_url = "https://contoh-situs-jadwal-transportasi-publik.com/rute"
        
        headers = {"User-Agent": "PatchTripThesis-Scraper/1.0"}
        
        # Contoh blok try-except untuk request HTTP web scraping
        # response = requests.get(target_url, headers=headers, timeout=15)
        # if response.status_code == 200:
        #     soup = BeautifulSoup(response.text, 'html.parser')
        #     # Lakukan ekstraksi elemen HTML target di sini...
        
        # SIMULASI HASIL EKSTRAKSI NYATA (Data hasil parsing web):
        # Anggap ini adalah data mentah yang berhasil diekstrak dari halaman web target hari ini
        scraped_data_list = [
            {
                "transport_type": "train",
                "provider_name": "KAI Eksekutif",
                "origin_city": "Jakarta",
                "destination_city": "Yogyakarta",
                "base_price": 350000.00,
                "departure": datetime(2026, 6, 15, 8, 0, 0),
                "arrival": datetime(2026, 6, 15, 16, 30, 0)
            }
        ]

        # Proses penyimpanan cerdas ke PostgreSQL (Upsert / Simpan baru)
        for item in scraped_data_list:
            # Cek apakah rute master sudah ada di database
            route = db.query(TransportRouteModel).filter_by(
                origin_city=item["origin_city"],
                destination_city=item["destination_city"],
                provider_name=item["provider_name"]
            ).first()

            if not route:
                # Jika belum ada, buat rute master baru
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

            # Tambahkan jadwal spesifik baru
            schedule = TransportScheduleModel(
                route_id=route.id,
                departure_time=item["departure"],
                arrival_time=item["arrival"],
                status="AVAILABLE"
            )
            db.add(schedule)
            db.commit()

        print("Background Worker: Scraping dan penyimpanan data ke PostgreSQL berhasil!")

    except Exception as e:
        print(f"Background Worker Error saat scraping: {e}")
        db.rollback()
    finally:
        db.close()