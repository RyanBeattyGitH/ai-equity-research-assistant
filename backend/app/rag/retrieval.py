from sqlalchemy import text
from app.db.session import SessionLocal


def search_similar_chunks(
    query_embedding,
    limit: int = 5,
    ticker: str | None = None
):
    db = SessionLocal()

    try:
        stmt = text("""
            SELECT
                ticker,
                filing_type,
                filing_year,
                section_type,
                chunk_text,
                embedding <-> CAST(:query_embedding AS vector) AS distance
            FROM document_chunks
            WHERE (:ticker IS NULL OR ticker = :ticker)
            ORDER BY
                embedding <-> CAST(:query_embedding AS vector)
            LIMIT :limit
        """)

        result = db.execute(
            stmt,
            {
                "query_embedding": query_embedding,
                "ticker": ticker,
                "limit": limit,
            }
        )

        return result.mappings().all()

    finally:
        db.close()
