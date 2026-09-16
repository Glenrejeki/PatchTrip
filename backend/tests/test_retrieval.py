import pytest
from unittest.mock import patch, MagicMock
from app.services.retrieval_service import RetrievalService

@patch("app.services.retrieval_service.faiss.read_index")
@patch("app.services.retrieval_service.os.path.exists", return_value=True)
def test_retrieval_service(mock_exists, mock_faiss_read):
    """
    Unit Test untuk menguji modul Semantic Dense Retrieval dengan mocking file index.
    """
    # Mocking objek FAISS index dan model embedding agar test dapat berjalan tanpa file fisik asli
    mock_index = MagicMock()
    mock_index.search.return_value = ([[0.1, 0.2]], [[0, 1]])
    mock_faiss_read.return_value = mock_index

    retriever = RetrievalService()
    retriever.metadata = [
        {"poi_id": 1, "name": "Candi Prambanan", "category": "Budaya"},
        {"poi_id": 2, "name": "Pantai Kuta", "category": "Pantai"}
    ]
    
    # Mocking model BGE-M3 encode agar tidak memuat beban model besar saat unit test
    mock_model = MagicMock()
    mock_model.encode.return_value = {"dense_vecs": [[0.1] * 768]}
    retriever.model = mock_model

    # Eksekusi fungsi retrieval
    query = "Pengguna menyukai wisata budaya dan candi."
    results = retriever.retrieve_relevant_pois(query_profile=query, top_k=2)

    # Validasi hasil keluaran
    assert isinstance(results, list), "Hasil retrieval harus berupa list data POI."
    assert len(results) <= 2, "Jumlah hasil tidak boleh melebihi parameter top_k."
    print("[TEST PASSED] test_retrieval_service berhasil dijalankan.")