import os
import re
from typing import List, Dict

from bs4 import BeautifulSoup
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

            with open(
                filing_path,
                "r",
                errors="ignore"
            ) as f:
                filing_text = f.read()

            # ------------------------------------
            # CLEAN SEC TEXT
            # ------------------------------------

            clean_text = clean_sec_text(filing_text)

            print(f"🧹 Cleaned text length: {len(clean_text):,} characters")

            chunks = chunk_text(clean_text)

            print(f"✂️ Total chunks: {len(chunks)}")

            # ------------------------------------
            # RESET PER FILE
            # ------------------------------------

            rows_for_file: List[Dict] = []

            # ------------------------------------
            # EMBEDDINGS
            # ------------------------------------

            for start in range(
                0,
                len(chunks),
                EMBED_BATCH_SIZE
            ):

                end = min(
                    start + EMBED_BATCH_SIZE,
                    len(chunks)
                )

                chunk_batch = chunks[start:end]

                print(
                    f"🧠 Embedding batch "
                    f"{start} → {end}"
                )

                batch_embeddings = get_embeddings(
                    chunk_batch
                )

                for chunk, embedding in zip(
                    chunk_batch,
                    batch_embeddings
                ):

                    # ------------------------------------
                    # BOILERPLATE FILTER
                    # ------------------------------------

                    if is_boilerplate(chunk):
                        continue

                    rows_for_file.append(
                        {
                            "chunk_text": chunk,
                            "embedding": embedding,
                            "ticker": ticker,
                            "filing_type": filing_type,
                            "filing_year": extract_year(
                                filing_path
                            ),
                            "section_type": classify_section(
                                chunk
                            ),
                        }
                    )

            print(
                f"📊 Usable chunks for file: "
                f"{len(rows_for_file)}"
            )

            # ------------------------------------
            # DATABASE INSERT
            # ------------------------------------

            for start in range(
                0,
                len(rows_for_file),
                DB_BATCH_SIZE
            ):

                end = min(
                    start + DB_BATCH_SIZE,
                    len(rows_for_file)
                )

                batch = rows_for_file[start:end]

                _flush_batch(
                    db,
                    batch
                )

                total_inserted += len(batch)

        db.commit()

        print(
            f"\n✅ DONE. Inserted "
            f"{total_inserted} chunks"
        )

    except Exception as e:

        db.rollback()

        print(
            f"❌ GLOBAL ERROR: {e}"
        )

        raise

    finally:

        db.close()


# --------------------------------------------------
# CLEANING
# --------------------------------------------------

def clean_sec_text(text: str) -> str:
    """
    Convert an SEC filing into readable text while
    removing SEC/XBRL/HTML boilerplate.
    """

    # --------------------------------------------------
    # 1. Extract DOCUMENT section
    # --------------------------------------------------

    match = re.search(
        r"<DOCUMENT>(.*?)</DOCUMENT>",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )

    if match:
        text = match.group(1)

    # --------------------------------------------------
    # 2. Parse HTML
    # --------------------------------------------------

    soup = BeautifulSoup(
        text,
        "lxml"
    )

    # Remove metadata/code elements
    for tag in soup([
        "script",
        "style",
        "head",
    ]):
        tag.decompose()


    # --------------------------------------------------
    # 3. Convert HTML tables to Markdown
    # --------------------------------------------------

    for table in soup.find_all("table"):

        rows = []

        for tr in table.find_all("tr"):

            cells = tr.find_all(["th", "td"])

            if not cells:
                continue

            row = []

            for cell in cells:

                value = " ".join(cell.stripped_strings).strip()

                if not value:
                    continue

                row.append(value)

            if row:
                rows.append(row)

        if not rows:
            continue

        # --------------------------------------------------
        # Merge split financial values
        # --------------------------------------------------

        cleaned_rows = []

        for row in rows:

            cleaned_row = []

            i = 0

            while i < len(row):

                current = row[i]

                # ------------------------------------------
                # Merge "$" + number
                # ------------------------------------------

                if (
                    current == "$"
                    and i + 1 < len(row)
                ):
                    cleaned_row.append(
                        "$" + row[i + 1]
                    )

                    i += 2
                    continue

                # ------------------------------------------
                # Merge number + "%"
                # ------------------------------------------

                if (
                    i + 1 < len(row)
                    and row[i + 1] == "%"
                ):
                    if current == "—":
                        cleaned_row.append("—")
                    else:
                        cleaned_row.append(current + "%")

                    i += 2
                    continue

                cleaned_row.append(current)

                i += 1

            cleaned_rows.append(cleaned_row)

            # Remove trailing empty cells from every row
            for row in rows:
                 while row and row[-1] == "":
                    row.pop()

        # --------------------------------------------------
        # Determine maximum number of columns
        # --------------------------------------------------

        column_count = max(
            len(row)
            for row in rows
        )

        # --------------------------------------------------
        # Pad rows so Markdown is valid
        # --------------------------------------------------

        for row in rows:

            while len(row) < column_count:
                row.append("")

        # --------------------------------------------------
        # Identify likely header
        # --------------------------------------------------

        header = rows[0]

        # If the first row consists mostly of years,
        # prepend a useful label for the first column.
        if (
            header
            and all(
                cell.isdigit() or cell in {"Change", ""}
                for cell in header
            )
        ):
            header = [""] + header

            while len(header) < column_count:
                header.append("")

        # --------------------------------------------------
        # Build Markdown
        # --------------------------------------------------

        markdown_table = []

        markdown_table.append(
            "| " + " | ".join(header) + " |"
        )

        markdown_table.append(
            "| "
            + " | ".join(
                ["---"] * len(header)
            )
            + " |"
        )

        for row in rows[1:]:

            markdown_table.append(
                "| " + " | ".join(row) + " |"
            )

        table_markdown = "\n".join(
            markdown_table
        )

        # --------------------------------------------------
        # Replace HTML table
        # --------------------------------------------------

        table.replace_with(
            soup.new_string(
                "\n\n"
                + table_markdown
                + "\n\n"
            )
        )

    # --------------------------------------------------
    # 3.5. Extract visible text
    # --------------------------------------------------

    text = soup.get_text(
        separator="\n"
    )

    # --------------------------------------------------
    # 4. Remove obvious XBRL noise
    # --------------------------------------------------

    lines = []

    for line in text.splitlines():

        line = line.strip()

        if not line:
            continue

        if line.startswith("xbrli:"):
            continue

        if line.startswith("xbrldi:"):
            continue

        if "http://www.sec.gov/" in line:
            continue

        if "http://fasb.org/" in line:
            continue

        lines.append(line)

    text = "\n".join(lines)

    # --------------------------------------------------
    # 5. Normalize whitespace
    # --------------------------------------------------

    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )

    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text
    )

    return text.strip()


def is_boilerplate(chunk: str) -> bool:
    """
    Filters out non-informative SEC/XBRL metadata.
    """

    text = chunk.lower()

    junk_signals = [
        "accession number",
        "conformed submission",
        "public document count",
        "mail address",
        "former company",
        "sec-header",
        "xbrli:",
        "xbrldi:",
        "explicitmember",
        "central index key",
        "standard industrial classification",
        "irs number",
        "film number",
        "sec file number",
    ]

    matches = sum(
        signal in text
        for signal in junk_signals
    )

    return matches >= 2


# --------------------------------------------------
# DATABASE INSERT
# --------------------------------------------------

def _flush_batch(
    db: Session,
    batch_rows: List[Dict]
):

    if not batch_rows:
        return

    stmt = insert(
        DocumentChunk
    )

    db.execute(
        stmt,
        batch_rows
    )

    print(
        f"💾 Inserted batch of "
        f"{len(batch_rows)}"
    )


# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def extract_year(
    filing_path: str
) -> int:

    try:

        accession = filing_path.split("/")[-2]

        return (
            2000
            + int(
                accession.split("-")[1]
            )
        )

    except Exception:

        return 0


def classify_section(chunk: str) -> str:

    text = chunk.lower()

    # Risk factors
    if (
        "risk factors" in text
        or "business risks" in text
        or "macroeconomic and industry risks" in text
    ):
        return "risk_factors"

    # Management discussion
    if (
        "management's discussion" in text
        or "management’s discussion" in text
        or "results of operations" in text
    ):
        return "md&a"

    # Financial statements
    if (
        "financial statements" in text
        or "consolidated statements" in text
        or "balance sheets" in text
        or "statements of operations" in text
    ):
        return "financials"

    # Business description
    if (
        "business overview" in text
        or "products and services" in text
    ):
        return "business"

    return "other"
