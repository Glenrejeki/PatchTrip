from fastapi import APIRouter
from app.api.v1.endpoints import compression, retrieval, generator

# Inisialisasi APIRouter utama untuk API version 1
api_router = APIRouter()

# Menghubungkan endpoint kompresi hierarkis (Hierarchical Patch Compression)
api_router.include_router(
    compression.router, 
    prefix="/compression", 
    tags=["Hierarchical Patch Compression"]
)

# Menghubungkan endpoint semantic dense retrieval (BGE-M3 & FAISS)
api_router.include_router(
    retrieval.router, 
    prefix="/retrieval", 
    tags=["Semantic Dense Retrieval"]
)

# Menghubungkan endpoint RAG & generasi itinerary LLM (Qwen3-8B)
api_router.include_router(
    generator.router, 
    prefix="/generator", 
    tags=["RAG & Itinerary Generation"]
)