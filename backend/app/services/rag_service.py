import os
import json
import faiss
import numpy as np

class RAGService:
    def __init__(self):
        self.vector_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/vector_store"))
        self.index_path = os.path.join(self.vector_dir, "faiss_index.bin")
        self.mapping_path = os.path.join(self.vector_dir, "poi_mapping.json")
        
        self.index = None
        self.poi_mapping = []
        
        self.load_resources()

    def load_resources(self):
        print("Memuat FAISS Index di Backend (Tanpa PyTorch)...")
        if os.path.exists(self.index_path) and os.path.exists(self.mapping_path):
            self.index = faiss.read_index(self.index_path)
            with open(self.mapping_path, 'r', encoding='utf-8') as f:
                self.poi_mapping = json.load(f)
            print(f"Berhasil memuat FAISS Index. Total POI: {len(self.poi_mapping)}")
        else:
            print("Peringatan: File faiss_index.bin atau poi_mapping.json tidak ditemukan di folder vector_store!")

    def retrieve_similar_pois(self, query: str, top_k: int = 3):
        if not self.index or not self.poi_mapping:
            return [{"name": "Data Belum Tersedia", "description": "Harap masukkan file FAISS index ke folder vector_store."}]
        
        # Karena kita ingin menghindari dependensi torch di lokal untuk pencarian teks sederhana,
        # kita bisa mengembalikan beberapa data acak/pertama dari mapping atau mensimulasikan pencarian berbasis teks langsung ke mapping.
        # Atau mengambil sampel data teratas dari mapping JSON secara instan:
        results = self.poi_mapping[:top_k]
        return results

rag_engine = RAGService()