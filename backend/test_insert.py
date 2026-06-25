# test_insert.py

from app.db.session import SessionLocal
from app.models.document_chunk import DocumentChunk
from app.embeddings import embed_text

db = SessionLocal()

embedding = list(embed_text("test chunk"))

row = DocumentChunk(
    chunk_text="test chunk",
    embedding=embedding,
    ticker="TEST",
    filing_type="10-K",
    filing_year=2025,
    section_type="other"
)

db.add(row)
db.commit()

print("SUCCESS")
