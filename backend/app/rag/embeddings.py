from openai import OpenAI
import os

# -----------------------------
# Client init (FIX)
# -----------------------------

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


# -----------------------------
# SINGLE EMBEDDING (optional legacy)
# -----------------------------

def get_embedding(text: str) -> list[float]:
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding


# -----------------------------
# BATCH EMBEDDING (NEW - USED IN INGEST)
# -----------------------------

def get_embeddings(texts: list[str]) -> list[list[float]]:
    """
    Batch embedding call (FAST)
    """
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=texts
    )

    return [item.embedding for item in response.data]
