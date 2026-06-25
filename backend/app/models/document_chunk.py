from sqlalchemy import Column, Integer, Text, String
from pgvector.sqlalchemy import Vector
from app.db.base import Base


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True, index=True)

    # Core content
    chunk_text = Column(Text, nullable=False)

    # Embedding vector
    embedding = Column(Vector(1536))

    # 🔥 NEW: financial metadata (this is what you're missing)
    ticker = Column(String, index=True)
    filing_type = Column(String)        # 10-K, 10-Q
    filing_year = Column(Integer)
    section_type = Column(String)       # risk_factors, md&a, business
