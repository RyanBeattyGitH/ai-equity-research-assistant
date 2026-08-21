from app.sec.ingest_filings import ingest_filings


if __name__ == "__main__":
    ingest_filings(
        ticker="AAPL",
        filing_type="10-K",
        limit=5,
    )
