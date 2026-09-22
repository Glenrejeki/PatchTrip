from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.services.retrieval_service import RetrievalService

router = APIRouter()

class RetrievalRequest(BaseModel):
    query_profile: str
    top_k: Optional[int] = 5

@router.post("/retrieve", summary="Semantic Retrieval POI")
async def retrieve_pois(payload: RetrievalRequest):
    """
    Endpoint untuk mencari rekomendasi POI yang relevan 
    berdasarkan profil preferensi menggunakan FAISS vector store.
    """
    try:
        retriever = RetrievalService()
        results = retriever.retrieve_relevant_pois(payload.query_profile, top_k=payload.top_k)
        
        return {
            "status": "success",
            "query_profile": payload.query_profile,
            "total_results": len(results),
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))