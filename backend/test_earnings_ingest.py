from app.services.earnings_ingest import ingest_earnings_calls
from app.db.session import SessionLocal
from app.models.document_chunk import DocumentChunk


def test_ingestion():
    symbol = "AAPL"

    print(f"\n🚀 Ingesting earnings calls for {symbol}...\n")

    ingest_earnings_calls(symbol, limit=1)

    print("\n📊 Checking database...\n")

    db = SessionLocal()

    rows = db.query(DocumentChunk).filter(
        DocumentChunk.ticker == symbol,
        DocumentChunk.source_type == "earnings_call"
    ).limit(5).all()

    for r in rows:
        print("-----")
        print("Ticker:", r.ticker)
        print("Type:", r.source_type)
        print("Text:", r.chunk_text[:200])

    db.close()

    print("\n✅ Test complete")


if __name__ == "__main__":
    test_ingestion()
