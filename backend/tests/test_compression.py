import pytest
from app.services.compression_service import CompressionService

def test_hierarchical_compression():
    """
    Unit Test untuk menguji modul 3-Level Patch Compression (Item -> Trip -> Profile).
    """
    compressor = CompressionService()
    
    # Data dummy riwayat perjalanan mentah untuk pengujian
    sample_raw_trips = [
        {
            "trip_id": "trip_1",
            "trip_name": "Liburan Pantai",
            "items": [
                {"name": "Pantai Kuta", "category": "Pantai"},
                {"name": "Pantai Sanur", "category": "Pantai"}
            ]
        }
    ]

    # Jalankan proses kompresi hierarkis
    profile = compressor.hierarchical_compress(sample_raw_trips)

    # Validasi hasil keluaran
    assert isinstance(profile, str), "Hasil kompresi harus berupa string teks profil."
    assert len(profile) > 0, "Profil preferensi tidak boleh kosong."
    assert "Profil Preferensi Implisit" in profile, "Format profil harus sesuai dengan standar modul."
    print("[TEST PASSED] test_hierarchical_compression berhasil dijalankan.")