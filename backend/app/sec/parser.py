import os
from bs4 import BeautifulSoup


def extract_filing_text(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # Try HTML parsing ONLY if it looks like HTML
    if "<html" in content.lower() or "<body" in content.lower():
        soup = BeautifulSoup(content, "lxml")

        for tag in soup(["script", "style"]):
            tag.decompose()

        return " ".join(soup.get_text(separator=" ").split())

    # Otherwise treat as raw text (IMPORTANT FIX)
    return " ".join(content.split())
