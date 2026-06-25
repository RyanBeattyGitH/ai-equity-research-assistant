from app.rag.retrieval import search_similar_chunks

query = "What are Nvidia's risks related to supply chain?"

results = search_similar_chunks(query)

print("\n=== TOP RESULTS ===\n")

for r in results:
    print(r["distance"])
    print(r["chunk_text"][:300])
    print("---")
