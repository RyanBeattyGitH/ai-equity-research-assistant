from app.rag.embeddings import get_embedding
from app.rag.retrieval import search_similar_chunks


query = "What was Apple's total net sales in 2025?"


# 1. Convert the question into an embedding
query_embedding = get_embedding(query)


# 2. Search only Apple's filings
results = search_similar_chunks(
    query_embedding=query_embedding,
    limit=5,
    ticker="AAPL",
)


print("\n=== TOP RESULTS ===\n")


# 3. Display the results
for i, r in enumerate(results, start=1):

    print(f"RESULT {i}")
    print(f"Distance: {r['distance']}")
    print(f"Ticker: {r['ticker']}")
    print(f"Year: {r['filing_year']}")
    print(f"Section: {r['section_type']}")

    print("\nText:")
    print(r["chunk_text"][:1000])

    print("\n" + "-" * 80)
