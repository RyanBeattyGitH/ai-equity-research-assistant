from sec_edgar_downloader import Downloader

# REQUIRED: use a real email (SEC requirement)
dl = Downloader("data", email_address="ryanbeatsbe@hotmail.com")

companies = ["AAPL", "MSFT", "TSLA", "JPM", "NVDA"]

for ticker in companies:
    print(f"Downloading {ticker} 10-K filings...")
    dl.get("10-K", ticker, limit=5)

print("Done.")
