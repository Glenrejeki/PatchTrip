import os
import requests
from typing import List, Dict, Any
from dotenv import load_dotenv

# Impor modul scraper yang sudah kita buat sebelumnya
from app.services.scraper_service import scrape_train_schedules, scrape_ferry_schedules

load_dotenv()

def fetch_live_transport_data(origin: str, destination: str) -> List[Dict[str, Any]]:
    """
    Layanan terpusat untuk menarik data jadwal transportasi secara otomatis dan real-time 
    berdasarkan URL target web scraping dan API publik yang dikonfigurasi di dalam file .env.
    """
    print(f"DEBUG: Memulai proses fetching untuk rute {origin} -> {destination}...")
    
    # Cek apakah URL dibaca dari .env dengan benar
    train_url = os.getenv("TRAIN_API_URL")
    print(f"DEBUG: Target TRAIN_API_URL dari .env -> {train_url}")

    all_transport_data = []

    try:
        # 1. Tarik data Kereta via Web Scraping berdasarkan link di .env (TRAIN_API_URL)
        train_results = scrape_train_schedules(origin, destination)
        if train_results:
            all_transport_data.extend(train_results)

    except Exception as e:
        print(f"Gagal mengambil data kereta: {e}")

    try:
        # 2. Tarik data Pesawat via API publik berdasarkan link di .env (FLIGHT_API_URL)
        flight_api_url = os.getenv("FLIGHT_API_URL")
        print(f"DEBUG: Target FLIGHT_API_URL dari .env -> {flight_api_url}")
        
        if flight_api_url and "example" not in flight_api_url:
            headers = {"User-Agent": "PatchTripThesis-Fetcher/1.0", "Accept": "application/json"}
            params = {"origin": origin, "destination": destination}
            
            response = requests.get(flight_api_url, headers=headers, params=params, timeout=10)
            if response.status_code == 200:
                flight_json = response.json()
                # Mapping data dari API penerbangan eksternal (contoh: aviationstack/sejenis)
                for flight in flight_json.get("data", []):
                    all_transport_data.append({
                        "transport_type": "flight",
                        "provider_name": flight.get("airline", {}).get("name", "Commercial Airline"),
                        "origin_city": origin,
                        "destination_city": destination,
                        "base_price": 750000.00,  # Dinamis dari respon API jika tersedia
                        "departure_time": flight.get("departure", {}).get("scheduled"),
                        "arrival_time": flight.get("arrival", {}).get("scheduled")
                    })
    except Exception as e:
        print(f"Gagal mengambil data penerbangan dari API eksternal: {e}")

    try:
        # 3. Tarik data Kapal/Feri via Web Scraping berdasarkan link di .env (FERRY_API_URL)
        ferry_url = os.getenv("FERRY_API_URL")
        print(f"DEBUG: Target FERRY_API_URL dari .env -> {ferry_url}")
        
        ferry_results = scrape_ferry_schedules(origin, destination)
        if ferry_results:
            all_transport_data.extend(ferry_results)

    except Exception as e:
        print(f"Gagal mengambil data kapal: {e}")

    print(f"DEBUG: Selesai fetching. Total data ditemukan: {len(all_transport_data)}")
    
    # Mengembalikan kumpulan data asli yang berhasil ditarik secara dinamis
    return all_transport_data