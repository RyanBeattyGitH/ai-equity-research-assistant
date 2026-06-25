from openai import OpenAI
from dotenv import load_dotenv
import os

from app.rag.embeddings import get_embedding
from app.rag.retrieval import search_similar_chunks
from app.rag.prompt import build_prompt

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def ask_rag(question: str):

    # 1. Embed question (ONLY HERE)
    query_embedding = get_embedding(question)

    # 2. Retrieve chunks using vector
    chunks = search_similar_chunks(query_embedding)

    # 3. Build prompt
    prompt = build_prompt(question, chunks)

    # 4. LLM call
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a financial analyst."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content
