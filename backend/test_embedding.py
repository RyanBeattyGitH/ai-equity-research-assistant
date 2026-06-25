# test_embedding.py

from app.embeddings import embed_text

embedding = embed_text("Apple sells iPhones.")

print(type(embedding))
print(len(embedding))

print(embedding[:5])
