import os
import pickle
import faiss
import numpy as np
from FlagEmbedding import BGEM3FlagModel
from typing import List, Dict, Any

class RetrievalService:
    def __init__(self):
        # Mengambil konfigurasi path vector store dan model embedding dari environment variables
        self.vector_store_path = os.getenv("VECTOR_STORE_PATH", "backend/data/vector_store")
        self.model_name = os.getenv("EMBEDDING_MODEL_PATH", "BAAI/bge-m3")
        
        # Lokasi file indeks FAISS dan metadata teks POI
        self.index_file = os.path.join(self.vector_store_path, "bge_m3_poi.index")
        self.metadata_file = os.path.join(self.vector_store_path, "poi_metadata.pkl")
        
        # Inisialisasi awal variabel dengan teknik lazy loading untuk efisiensi memori
        self.model = None
        self.index = None
        self.metadata = None

    def _load_resources(self):
        """
        Memuat model embedding BGE-M3, file indeks biner FAISS, dan metadata teks ke dalam memori.
        """
        if self.model is None:
            # Memuat model BGE-M3 untuk menghasilkan dense embedding multibahasa & multigranular
            self.model = BGEM3FlagModel(self.model_name, use_fp16=True)
            
        if self.index is None and os.path.exists(self.index_file):
            # Memuat file indeks FAISS untuk pencarian kedekatan vektor (ANN Search)
            self.index = faiss.read_index(self.index_file)
            
        if self.metadata is None and os.path.exists(self.metadata_file):
            # Memuat metadata teks asli POI yang dipetakan berdasarkan ID vektor
            with open(self.metadata_file, "rb") as f:
                self.metadata = pickle.load(f)

    def retrieve_relevant_pois(self, query_profile: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Melakukan Semantic Dense Retrieval:
        Mengubah profil preferensi abstrak pengguna menjadi vektor angka, lalu mencari
        destinasi konkret di FAISS yang memiliki kedekatan makna semantik tertinggi.
        """
        self._load_resources()
        
        # Validasi ketat: Pastikan file indeks FAISS dan metadata lokal sudah di-generate sebelumnya
        if self.index is None or self.metadata is None:
            raise FileNotFoundError(
                f"Sumber data vector store tidak ditemukan di direktori: {self.vector_store_path}. "
                "Pastikan Anda telah menjalankan skrip indexing untuk menghasilkan file "
                "'bge_m3_poi.index' dan 'poi_metadata.pkl'."
            )

        # 1. Mengubah teks profil preferensi implisit menjadi dense vector menggunakan BGE-M3
        encoded_query = self.model.encode(
            [query_profile], 
            batch_size=1, 
            max_length=512
        )
        query_vector = np.array(encoded_query['dense_vecs']).astype('float32')

        # 2. Melakukan pencarian Approximate Nearest Neighbor (ANN) pada basis data vektor FAISS
        distances, indices = self.index.search(query_vector, top_k)

        # 3. Mengambil metadata teks asli berdasarkan indeks/ID POI yang dikembalikan oleh FAISS
        retrieved_results = []
        for i, idx in enumerate(indices[0]):
            if idx != -1 and idx < len(self.metadata):
                poi_info = self.metadata[idx]
                poi_info["similarity_score"] = float(distances[0][i])  # Menyisipkan skor kedekatan semantik
                retrieved_results.append(poi_info)

        return retrieved_results