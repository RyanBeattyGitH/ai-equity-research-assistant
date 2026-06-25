import os
from sec_edgar_downloader import Downloader
from dotenv import load_dotenv

load_dotenv()

SEC_EMAIL = os.getenv("SEC_EMAIL")

if not SEC_EMAIL:
    raise ValueError("Missing SEC_EMAIL in .env")

# Root download directory (this is what sec-edgar-downloader actually uses)
DOWNLOAD_ROOT = "data/sec-edgar-filings"

dl = Downloader(SEC_EMAIL, DOWNLOAD_ROOT)


def download_filings(ticker: str, filing_type: str = "10-K", limit: int = 2):
    """
    Download SEC filings and return list of full-submission.txt file paths.
    """

    # Step 1: download filings
    dl.get(filing_type, ticker, limit=limit)

    base_path = os.path.join(DOWNLOAD_ROOT, ticker, filing_type)

    if not os.path.exists(base_path):
        raise FileNotFoundError(
            f"Missing SEC path: {base_path}. "
            f"Check downloader output or SEC library structure."
        )

    filing_paths = []

    # Step 2: each accession folder contains full-submission.txt
    for accession_folder in os.listdir(base_path):
        full_path = os.path.join(
            base_path,
            accession_folder,
            "full-submission.txt"
        )

        if os.path.exists(full_path):
            filing_paths.append(full_path)

    if not filing_paths:
        raise FileNotFoundError(
            f"No full-submission.txt files found for {ticker} in {base_path}"
        )

    print(f"📦 Downloaded {len(filing_paths)} filings for {ticker}")

    return filing_paths
