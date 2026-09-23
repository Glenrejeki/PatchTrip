from app.services.scraper_service import scrape_sisparnas_attractions, scrape_agoda_accommodations

def sync_national_tourism_data(city: str):
    print(f"Menarik data pariwisata nasional untuk wilayah: {city}")
    
    # 1. Tarik data tempat wisata dari SISPARNAS
    sisparnas_data = scrape_sisparnas_attractions(city)
    
    # 2. Tarik data akomodasi dari Agoda
    agoda_data = scrape_agoda_accommodations(city)
    
    # 3. Proses dan simpan hasilnya ke database PostgreSQL via SQLAlchemy session
    # ... simpan ke tabel POI / accommodations lokal Anda ...
    
    return {
        "attractions_fetched": len(sisparnas_data),
        "accommodations_fetched": len(agoda_data)
    }