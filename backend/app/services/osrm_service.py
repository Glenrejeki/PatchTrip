import requests

OSRM_URL = "http://router.project-osrm.org/route/v1/driving"

def get_travel_time_matrix(lat1: float, lon1: float, lat2: float, lon2: float):
    """Menghitung estimasi durasi (menit) dan jarak (km) antara dua koordinat via OSRM"""
    url = f"{OSRM_URL}/{lon1},{lat1};{lon2},{lat2}?overview=false"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data.get("routes"):
                route = data["routes"][0]
                distance_km = route["distance"] / 1000.0  # Konversi meter ke km
                duration_minutes = route["duration"] / 60.0 # Konversi detik ke menit
                return round(distance_km, 2), round(duration_minutes, 1)
    except Exception as e:
        print(f"OSRM Error: {e}")
    
    return 0.0, 0.0