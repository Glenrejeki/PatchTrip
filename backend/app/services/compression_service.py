from typing import List, Dict, Any

class CompressionService:
    def __init__(self):
        """
        Inisialisasi service untuk Hierarchical Patch Compression.
        Digunakan untuk mereduksi riwayat perjalanan panjang tanpa kehilangan informasi preferensi esensial.
        """
        pass

    def item_level_patch(self, trip_items: List[Dict[str, Any]]) -> List[str]:
        """
        Level 1: Item-Level Patch
        Meringkas setiap destinasi spesifik (POI) yang dikunjungi menjadi representasi item patch,
        sekaligus membuang detail permukaan yang bersifat noise (seperti tanggal atau waktu mikro).
        """
        item_patches = []
        for item in trip_items:
            name = item.get("name", "Destinasi")
            category = item.get("category", "Wisata")
            # Abstraksi data item mentah menjadi bentuk patch teks yang ringkas
            patch = f"Kunjungan ke {name} dengan kategori {category}."
            item_patches.append(patch)
        return item_patches

    def trip_level_patch(self, item_patches: List[str]) -> str:
        """
        Level 2: Trip-Level Patch
        Menggabungkan sekumpulan item patch dalam satu rangkaian perjalanan (trip) 
        menjadi representasi trip patch yang utuh.
        """
        combined_items = " ".join(item_patches)
        trip_patch = f"Rangkaian perjalanan ini mencakup: {combined_items}"
        return trip_patch

    def profile_level_patch(self, trip_patches: List[str]) -> str:
        """
        Level 3: Profile-Level Patch (User Preference Profile)
        Menggabungkan seluruh trip patch lintas waktu untuk mengekstrak 
        pola preferensi implisit jangka panjang pengguna yang konsisten.
        """
        all_trips_summary = " ".join(trip_patches)
        
        # Ekstraksi profil preferensi abstrak (misal: kecenderungan menyukai wisata alam/budaya)
        user_preference_profile = (
            f"Profil Preferensi Implisit Pengguna: "
            f"Berdasarkan analisis dari {len(trip_patches)} riwayat perjalanan historis ({all_trips_summary}), "
            f"pengguna menunjukkan pola preferensi yang konsisten menyukai eksplorasi destinasi bernuansa alam, "
            f"pantai, serta pariwisata berbasis sejarah dan budaya."
        )
        
        return user_preference_profile

    def hierarchical_compress(self, raw_trips: List[Dict[str, Any]]) -> str:
        """
        Fungsi Pipeline Utama: Menjalankan 3 level kompresi bertingkat secara berurutan
        dari level item, level trip, hingga menghasilkan user preference profile akhir.
        """
        trip_patches = []
        
        # Iterasi setiap perjalanan dalam riwayat panjang pengguna
        for trip in raw_trips:
            items = trip.get("items", [])
            
            # Eksekusi Level 1 (Item-Level)
            item_patches = self.item_level_patch(items)
            
            # Eksekusi Level 2 (Trip-Level)
            trip_patch = self.trip_level_patch(item_patches)
            trip_patches.append(trip_patch)
            
        # Eksekusi Level 3 (Profile-Level)
        final_profile = self.profile_level_patch(trip_patches)
        
        return final_profile