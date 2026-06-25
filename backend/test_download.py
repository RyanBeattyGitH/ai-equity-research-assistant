# test_download.py

from app.sec.download import download_10k

result = download_10k("AAPL", "10-K", limit=1)

print("TYPE:", type(result))
print("VALUE:", result)
