from sqlalchemy import text
from app.db.session import SessionLocal


def search_similar_chunks(query_embedding, limit: int = 5):
    db = SessionLocal()

    try:
        stmt = text("""
            SELECT
                chunk_text,
                embedding <-> CAST(:query_embedding AS vector) AS distance
            FROM document_chunks
            ORDER BY embedding <-> CAST(:query_embedding AS vector)
            LIMIT :limit
        """)

        result = db.execute(
            stmt,
            {
                "query_embedding": query_embedding,
                "limit": limit
            }
        )

        return result.mappings().all()

    finally:
        db.close()
