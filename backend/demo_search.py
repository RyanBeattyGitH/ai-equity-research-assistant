# demo_search.py

from app.db.session import SessionLocal
from app.models.document_chunk import DocumentChunk

db = SessionLocal()

results = (
    db.query(DocumentChunk)
      .filter(DocumentChunk.ticker == "AAPL")
      .limit(3)
      .all()
)

for r in results:
    print("Ticker:", r.ticker)
    print("Type:", r.filing_type)
    print("Text:", r.chunk_text[:300])
    print("-" * 80)
