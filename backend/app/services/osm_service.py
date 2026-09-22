import requests

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
OVERPASS_URL = "https://overpass-api.de/api/interpreter"

def get_city_coordinates(city_name: str):
    headers = {"User-Agent": "PatchTripThesis/1.0"}
    params = {"q": f"{city_name}, Indonesia", "format": "json", "limit": 1}
    try:
        response = requests.get(NOMINATIM_URL, params=params, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data:
                return float(data[0]["lat"]), float(data[0]["lon"])
    except Exception as e:
        print(f"Nominatim Error: {e}")
    return None, None

def fetch_pois_from_osm(city_name: str):
    lat, lon = get_city_coordinates(city_name)
    if not lat or not lon:
        print("Koordinat kota tidak ditemukan.")
        return []

    # Query dipersempit khusus node wisata/hotel terdekat (paling ringan agar tidak diblokir server)
    query = f"""
    [out:json][timeout:10];
    node["tourism"](around:3000,{lat},{lon});
    out body;
    """
    
    headers = {
        "User-Agent": "PatchTripThesis-StudentResearch/1.0 (thesis project)",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    try:
        print(f"Mengirim query ke Overpass API untuk kota {lat}, {lon}...")
        response = requests.post(OVERPASS_URL, data={'data': query}, headers=headers, timeout=15)
        
        print(f"Status Code dari Overpass: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            elements = data.get('elements', [])
            print(f"Jumlah elemen mentah ditemukan dari Overpass: {len(elements)}")
            
            pois = []
            for el in elements:
                tags = el.get('tags', {})
                if 'name' in tags:
                    pois.append({
                        "id": str(el.get('id')),
                        "name": tags['name'],
                        "city": city_name,
                        "category": tags.get('tourism', 'attraction'),
                        "lat": el.get('lat'),
                        "lon": el.get('lon'),
                        "description": tags.get('description', f"Lokasi {tags['name']} di {city_name}.")
                    })
            return pois
    except Exception as e:
        print(f"Overpass Error: {e}")
        
    return []