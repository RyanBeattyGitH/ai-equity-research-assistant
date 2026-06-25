def build_prompt(question: str, chunks):
    context = "\n\n".join([c["chunk_text"] for c in chunks])

    prompt = f"""
You are a financial analyst.

Use the context below to answer the question.

CONTEXT:
{context}

QUESTION:
{question}

Answer clearly and concisely.
"""
    return prompt
