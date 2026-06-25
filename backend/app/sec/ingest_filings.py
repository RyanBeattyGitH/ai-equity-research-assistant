import os
from typing import List, Dict

from sqlalchemy import insert
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.document_chunk import DocumentChunk

from app.sec.downloader import download_filings
from app.services.chunking import chunk_text
from app.rag.embeddings import get_embeddings


DB_BATCH_SIZE = int(os.getenv("DB_BATCH_SIZE", 500))
EMBED_BATCH_SIZE = int(os.getenv("EMBED_BATCH_SIZE", 100))


# --------------------------------------------------
# INGESTION
# --------------------------------------------------

def ingest_filings(
    ticker: str,
    filing_type: str = "10-K",
    limit: int | None = None,
):

    db: Session = SessionLocal()

    try:
        print(f"📥 Downloading {filing_type} for {ticker}...")

        filing_paths = download_filings(
            ticker,
            filing_type,
            limit=limit,
        )

        total_inserted = 0

        for filing_path in filing_paths:

            print(f"\n📄 Processing file: {filing_path}")

            # ------------------------------------
            # READ FILE
            # ------------------------------------
            with open(filing_path, "r", errors="ignore") as f:
                filing_text = f.read()

            chunks = chunk_text(filing_text)

            print(f"✂️ Total chunks: {len(chunks)}")

            # TEMP DEMO LIMIT
            chunks = chunks[:100]

            print(f"✂️ Using first {len(chunks)} chunks for demo")

            # --------------------------------------------------
            # IMPORTANT FIX: reset per file
            # --------------------------------------------------
            rows_for_file: List[Dict] = []

            # ------------------------------------
            # EMBEDDINGS (batched)
            # ------------------------------------
            for start in range(0, len(chunks), EMBED_BATCH_SIZE):

                end = min(start + EMBED_BATCH_SIZE, len(chunks))
                chunk_batch = chunks[start:end]

                print(f"🧠 Embedding batch {start} → {end}")

                batch_embeddings = get_embeddings(chunk_batch)

                for chunk, embedding in zip(chunk_batch, batch_embeddings):

                    rows_for_file.append(
                        {
                            "chunk_text": chunk,
                            "embedding": embedding,
                            "ticker": ticker,
                            "filing_type": filing_type,
                            "filing_year": extract_year(filing_path),
                            "section_type": classify_section(chunk),
                        }
                    )

            # ------------------------------------
            # DB INSERT (batched per file)
            # ------------------------------------
            for start in range(0, len(rows_for_file), DB_BATCH_SIZE):

                end = min(start + DB_BATCH_SIZE, len(rows_for_file))
                batch = rows_for_file[start:end]

                _flush_batch(db, batch)

                total_inserted += len(batch)

        db.commit()

        print(f"\n✅ DONE. Inserted {total_inserted} chunks")

    except Exception as e:

        db.rollback()
        print(f"❌ GLOBAL ERROR: {e}")
        raise

    finally:
        db.close()


# --------------------------------------------------
# BULK INSERT
# --------------------------------------------------

def _flush_batch(db: Session, batch_rows: List[Dict]):

    if not batch_rows:
        return

    stmt = insert(DocumentChunk)
    db.execute(stmt, batch_rows)

    print(f"💾 Inserted batch of {len(batch_rows)}")


# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def extract_year(filing_path: str) -> int:
    try:
        accession = filing_path.split("/")[-2]
        return 2000 + int(accession.split("-")[1])
    except:
        return 0


def classify_section(chunk: str) -> str:

    text = chunk.lower()

    if "risk factors" in text:
        return "risk_factors"

    if "management's discussion" in text:
        return "md&a"

    if "financial statements" in text:
        return "financials"

    return "other"
