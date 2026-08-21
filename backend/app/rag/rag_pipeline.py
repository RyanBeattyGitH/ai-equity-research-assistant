from openai import OpenAI
from dotenv import load_dotenv
import os

from app.rag.embeddings import get_embedding
from app.rag.retrieval import search_similar_chunks
from app.rag.prompt import build_prompt

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def ask_rag(question: str, ticker: str):

    # 1. Embed question
    query_embedding = get_embedding(question)

    # 2. Retrieve relevant chunks for this company
    chunks = search_similar_chunks(
        query_embedding=query_embedding,
        limit=5,
        ticker=ticker,
    )

    # 3. Build prompt
    prompt = build_prompt(question, chunks)

    # 4. Ask GPT
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an AI equity research assistant. "
                    "Use only the SEC filing context supplied by the user prompt. "
                    "Do not invent facts or introduce unsupported information. "
                    "If the evidence is insufficient, say so."
)
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    answer = response.choices[0].message.content

    # 5. Return answer + source information
    sources = [
        {
            "ticker": chunk["ticker"],
            "filing_type": chunk["filing_type"],
            "filing_year": chunk["filing_year"],
            "section_type": chunk["section_type"],
            "text": chunk["chunk_text"],
            "distance": float(chunk["distance"]),
        }
        for chunk in chunks
    ]

    return {
        "answer": answer,
        "sources": sources,
    }
