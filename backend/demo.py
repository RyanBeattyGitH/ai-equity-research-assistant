from sqlalchemy import text

from app.db.session import SessionLocal

db = SessionLocal()

rows = db.execute(
    text("""
    SELECT
        ticker,
        filing_type,
        LEFT(chunk_text, 500)
    FROM document_chunks
    LIMIT 3
    """)
)

for row in rows:
    print("=" * 80)
    print(f"Ticker: {row.ticker}")
    print(f"Type: {row.filing_type}")
    print()
    print(row.left)
