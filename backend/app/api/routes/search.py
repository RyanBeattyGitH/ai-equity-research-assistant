from fastapi import APIRouter
from pydantic import BaseModel

from app.rag.embeddings import get_embedding
from app.rag.retrieval import search_similar_chunks
from app.rag.rag_pipeline import ask_rag


router = APIRouter(
    prefix="/api",
    tags=["search"],
)


class SearchRequest(BaseModel):
    query: str
    ticker: str


@router.post("/search")
def search(request: SearchRequest):

    query_embedding = get_embedding(request.query)

    results = search_similar_chunks(
        query_embedding=query_embedding,
        limit=5,
        ticker=request.ticker,
    )

    return {
        "query": request.query,
        "ticker": request.ticker,
        "results": [
            {
                "ticker": result["ticker"],
                "filing_type": result["filing_type"],
                "filing_year": result["filing_year"],
                "section_type": result["section_type"],
                "text": result["chunk_text"],
                "distance": float(result["distance"]),
            }
            for result in results
        ],
    }


@router.post("/ask")
def ask(request: SearchRequest):

    result = ask_rag(
        question=request.query,
        ticker=request.ticker,
    )

    return {
        "query": request.query,
        "ticker": request.ticker,
        "answer": result["answer"],
        "sources": result["sources"],
    }
