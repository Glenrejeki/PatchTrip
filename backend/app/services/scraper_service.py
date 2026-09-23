import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

def scrape_sisparnas_attractions(city: str = None):
    """
    Melakukan web scraping data daya tarik wisata (DTW) dari portal resmi SISPARNAS Kemenparekraf.
    """
    url = os.getenv("SISPARNAS_URL", "https://sisparnas.kemenpar.go.id/datapanel")
    headers = {"User-Agent": "PatchTrip-ThesisBot/1.0"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            attractions = []
            # Contoh parsing elemen berdasarkan struktur panel data SISPARNAS
            # (Sesuaikan selector HTML dengan hasil Inspect Element di halaman datapanel SISPARNAS)
            cards = soup.find_all('div', class_='destination-card') # Ganti dengan class aktual
            
            for card in cards:
                name = card.find('h5').text.strip() if card.find('h5') else "Unknown Destination"
                location = card.find('span', class_='location').text.strip() if card.find('span', class_='location') else city
                
                attractions.append({
                    "name": name,
                    "category": "Wisata Alam/Budaya",
                    "city": location,
                    "source": "SISPARNAS Kemenparekraf"
                })
            return attractions
    except Exception as e:
        print(f"Gagal melakukan scraping SISPARNAS: {e}")
    
    return []

def scrape_agoda_accommodations(destination_query: str):
    """
    Mengambil data referensi akomodasi/hotel dari Agoda secara dinamis.
    Catatan: Agoda menggunakan proteksi ketat, sehingga scraper ini dirancang 
    sebagai struktur dasar pemanggilan target URL pencarian.
    """
    base_url = os.getenv("AGODA_TARGET_URL", "https://www.agoda.com")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept-Language": "id-ID,id;q=0.9"
    }

    try:
        # Contoh URL pencarian dinamis Agoda
        search_url = f"{base_url}/search?text={destination_query}"
        response = requests.get(search_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            accommodations = []
            
            # Karena Agoda banyak menggunakan render JavaScript (React/Next.js),
            # pastikan mengekstrak elemen penampung data hotel jika tersedia di HTML statis.
            hotel_elements = soup.find_all('h3', {'data-selenium': 'hotel-name'})
            
            for hotel in hotel_elements:
                accommodations.append({
                    "hotel_name": hotel.text.strip(),
                    "destination": destination_query,
                    "source": "Agoda"
                })
            return accommodations
    except Exception as e:
        print(f"Gagal melakukan scraping Agoda: {e}")
        
    return []