from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from app.similarity import local_similarity_search  # Assumes this function exists
from app.web_agent import find_similar_projects

router = APIRouter()

class SearchRequest(BaseModel):
    query: str
    top_n: int = 5

class SearchResult(BaseModel):
    title: str
    snippet: str = ""
    link: str = ""
    similarity: float
    source: str  # "local" or "web"

@router.post("/search_similarity", response_model=List[SearchResult])
def search_similarity(request: SearchRequest):
    try:
        # Local similarity search (pgvector)
        local_results = local_similarity_search(request.query, top_n=request.top_n)
        for res in local_results:
            res["source"] = "local"

        # Web similarity search
        web_results = find_similar_projects(request.query, top_n=request.top_n)
        for res in web_results:
            res["source"] = "web"

        # Combine and sort by similarity
        combined = local_results + web_results
        combined.sort(key=lambda x: x["similarity"], reverse=True)
        return combined
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))