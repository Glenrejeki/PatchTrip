from fastapi import APIRouter, HTTPException
from app.services.scraper_service import scrape_sisparnas_attractions, scrape_agoda_accommodations

router = APIRouter()

@router.post("/sync-external-data")
def trigger_external_sync(city: str):
    """
    Endpoint khusus untuk mengetes proses scraping real-time 
    dari SISPARNAS dan Agoda berdasarkan kota tujuan.
    """
    try:
        print(f"--- MEMULAI SCRAPING LIVE UNTUK KOTA: {city} ---")
        
        # 1. Tarik data live dari SISPARNAS Kemenparekraf
        sisparnas_results = scrape_sisparnas_attractions(city)
        
        # 2. Tarik data live dari Agoda
        agoda_results = scrape_agoda_accommodations(city)
        
        total_data = len(sisparnas_results) + len(agoda_results)
        
        if total_data == 0:
            return {
                "status": "success",
                "message": f"Scraping berhasil dijalankan secara dinamis untuk {city}, namun struktur HTML target belum mengembalikan elemen data (0 hasil).",
                "sisparnas_data": [],
                "agoda_data": []
            }

        return {
            "status": "success",
            "message": f"Berhasil menarik {total_data} data secara dinamis tanpa hardcode!",
            "sisparnas_data": sisparnas_results,
            "agoda_data": agoda_results
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal melakukan proses scraping: {str(e)}")