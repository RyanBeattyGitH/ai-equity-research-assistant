from app.services.chunking import chunk_text
from app.rag.embeddings import get_embedding
from app.models.document_chunk import DocumentChunk
from app.db.session import SessionLocal


def ingest_document(text: str):

    chunks = chunk_text(text)

    db = SessionLocal()

    try:
        for chunk in chunks:

            embedding = get_embedding(chunk)

            db_chunk = DocumentChunk(
                document_id=1,      # placeholder (you can improve later)
                chunk_text=chunk,   # ✅ FIXED (was "content")
                embedding=embedding
            )

            db.add(db_chunk)

        db.commit()

        print(f"Inserted {len(chunks)} chunks.")

    except Exception as e:
        db.rollback()
        raise e

    finally:
        db.close()
