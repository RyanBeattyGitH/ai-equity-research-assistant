from langchain_text_splitters import RecursiveCharacterTextSplitter


# SEC filings are large documents.
# These settings balance:
# - retrieval quality
# - embedding cost
# - ingestion speed

CHUNK_SIZE = 1500
CHUNK_OVERLAP = 200


splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    separators=[
        "\n\n",
        "\n",
        ". ",
        " ",
        ""
    ]
)


def chunk_text(text: str) -> list[str]:
    """
    Split filing text into overlapping chunks.

    Input:
        Full filing text

    Output:
        List[str]
    """

    if not text:
        return []

    text = text.strip()

    if not text:
        return []

    chunks = splitter.split_text(text)

    return [
        chunk.strip()
        for chunk in chunks
        if chunk.strip()
    ]
