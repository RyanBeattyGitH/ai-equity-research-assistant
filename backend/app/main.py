from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.rag.rag_pipeline import ask_rag


app = FastAPI(title="AI Equity Research Assistant")


# Allow the React frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SearchRequest(BaseModel):
    question: str
    ticker: str


@app.get("/")
def root():
    return {
        "message": "AI Equity Research Assistant API"
    }


@app.post("/api/search")
def search(request: SearchRequest):
    result = ask_rag(
        question=request.question,
        ticker=request.ticker,
    )

    return result
