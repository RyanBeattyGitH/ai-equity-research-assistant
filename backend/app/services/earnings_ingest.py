import os
import requests
from dotenv import load_dotenv

from app.services.chunking import chunk_text
from app.rag.embeddings import get_embedding
from app.models.document_chunk import DocumentChunk
from app.db.session import SessionLocal

load_dotenv()

FMP_API_KEY = os.getenv("FMP_API_KEY")


# ---------------------------
# 1. FETCH
# ---------------------------
def fetch_earnings_calls(symbol: str, limit: int = 1):
    if not FMP_API_KEY:
        raise ValueError("Missing FMP_API_KEY")

    url = "https://financialmodelingprep.com/api/v3/earning_call_transcript"

    params = {
        "symbol": symbol,
        "limit": limit,
        "apikey": FMP_API_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise Exception(f"FMP error {response.status_code}: {response.text}")

    return response.json()


# ---------------------------
# 2. INGEST PIPELINE
# ---------------------------
def ingest_earnings_calls(symbol: str, limit: int = 1):

    data = fetch_earnings_calls(symbol, limit)

    if not data:
        print("No earnings calls found")
        return

    db = SessionLocal()

    try:
        for item in data:

            # FMP structure varies → defensive parsing
            text = item.get("content") or item.get("text") or ""

            if not text:
                continue

            chunks = chunk_text(text)

            for chunk in chunks:
                embedding = get_embedding(chunk)

                db_chunk = DocumentChunk(
                    document_id=1,
                    chunk_text=chunk,
                    embedding=embedding
                )

                db.add(db_chunk)

        db.commit()

        print(f"Inserted earnings calls for {symbol}")

    except Exception as e:
        db.rollback()
        raise e

    finally:
        db.close()
