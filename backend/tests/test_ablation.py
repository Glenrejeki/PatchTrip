import pytest
from app.services.rag_service import RAGService
from app.services.compression_service import CompressionService
from app.services.retrieval_service import RetrievalService

class AblationStudyRunner:
    def __init__(self):
        self.compressor = CompressionService()
        self.rag = RAGService()

    def run_variant(self, variant_name: str, raw_trips, pois_candidates, constraints):
        """
        Menjalankan variasi model untuk keperluan pengujian Ablation Study.
        Variasi yang diuji:
        1. 'LLM_ONLY': Mengandalkan LLM murni tanpa profil kompresi dan tanpa retrieval eksternal.
        2. 'RETRIEVAL_ONLY': Menggunakan retrieval POI langsung tanpa kompresi riwayat hierarkis.
        3. 'PATCH_ONLY': Menggunakan hasil kompresi profil tanpa memperkaya konteks dengan retrieval POI.
        4. 'PATCHTRIP_FULL': Sistem lengkap (Kompresi Hierarkis + Semantic Retrieval + RAG LLM).
        """
        if variant_name == "LLM_ONLY":
            profile = "Pengguna umum."
            pois = []
        elif variant_name == "RETRIEVAL_ONLY":
            profile = "Pengguna umum tanpa riwayat terkompresi."
            pois = pois_candidates
        elif variant_name == "PATCH_ONLY":
            profile = self.compressor.hierarchical_compress(raw_trips)
            pois = []
        elif variant_name == "PATCHTRIP_FULL":
            profile = self.compressor.hierarchical_compress(raw_trips)
            pois = pois_candidates
        else:
            raise ValueError("Nama varian ablation study tidak valid.")

        # Eksekusi generasi RAG berdasarkan varian yang aktif
        result = self.rag.generate_itinerary(
            user_profile=profile,
            pois=pois,
            constraints=constraints
        )
        return result

def test_ablation_variants():
    """
    Unit Test untuk memastikan seluruh skema varian Ablation Study tereksekusi tanpa error.
    """
    runner = AblationStudyRunner()
    
    dummy_trips = [{"trip_id": "1", "items": [{"name": "Gunung Bromo", "category": "Alam"}]}]
    dummy_pois = [{"poi_id": 10, "name": "Kawah Ijen", "category": "Alam", "description": "Wisata kawah."}]
    constraints = {"duration_days": 2, "budget": "Menengah", "location": "Jawa Timur"}

    # Uji 4 varian konfigurasi ablation study
    variants = ["LLM_ONLY", "RETRIEVAL_ONLY", "PATCH_ONLY", "PATCHTRIP_FULL"]
    
    for v in variants:
        output = runner.run_variant(v, dummy_trips, dummy_pois, constraints)
        assert isinstance(output, str), f"Varian {v} harus menghasilkan output string itinerary."
        assert len(output) > 0, f"Varian {v} menghasilkan output kosong."

    print("[TEST PASSED] Seluruh varian Ablation Study berhasil divalidasi.")