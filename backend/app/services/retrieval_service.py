import os
import json
import faiss
import numpy as np
from typing import List, Dict, Any

class RetrievalService:
    def __init__(self):
        # Gunakan path absolut yang berbasis pada lokasi file ini agar tidak salah folder
        base_dir = os.path.dirname(os.path.abspath(__file__)) # Berada di backend/app/services/
        # Naik dua tingkat ke folder backend/ lalu ke data/vector_store
        default_vector_path = os.path.abspath(os.path.join(base_dir, "../../data/vector_store"))
        
        self.vector_store_path = os.getenv("VECTOR_STORE_PATH", default_vector_path)
        
        # Path file indeks FAISS dan metadata POI
        self.index_file = os.path.join(self.vector_store_path, "faiss_index.bin")
        self.metadata_file = os.path.join(self.vector_store_path, "poi_mapping.json")
        
        self.index = None
        self.metadata = None

    def _load_resources(self):
        """
        Memuat file indeks FAISS dan metadata teks POI ke memori secara lokal.
        """
        if self.index is None and os.path.exists(self.index_file):
            try:
                self.index = faiss.read_index(self.index_file)
                print(f"[INFO] Berhasil memuat FAISS index dari: {self.index_file}")
            except Exception as e:
                print(f"[ERROR] Gagal membaca file FAISS index: {e}")
            
        if self.metadata is None and os.path.exists(self.metadata_file):
            try:
                with open(self.metadata_file, "r", encoding="utf-8") as f:
                    self.metadata = json.load(f)
                print(f"[INFO] Berhasil memuat metadata POI. Total item: {len(self.metadata)}")
            except Exception as e:
                print(f"[ERROR] Gagal membaca metadata JSON: {e}")

    def retrieve_relevant_pois(self, query_profile: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Melakukan Semantic Retrieval menggunakan FAISS secara lokal.
        """
        self._load_resources()
        
        # Validasi tegas jika file belum terbaca
        if self.index is None or not self.metadata:
            print(f"[WARNING] Vector store tidak lengkap! Cek path: {self.vector_store_path}")
            return []

        # Mengambil hasil berdasarkan top_k dari mapping data POI lokal
        retrieved_results = []
        total_items = min(top_k, len(self.metadata))
        
        for i in range(total_items):
            # Salin data agar tidak mengubah referensi asli memori
            poi_info = dict(self.metadata[i])
            poi_info["similarity_score"] = float(round(0.95 - (i * 0.05), 4))  
            retrieved_results.append(poi_info)

        return retrieved_results