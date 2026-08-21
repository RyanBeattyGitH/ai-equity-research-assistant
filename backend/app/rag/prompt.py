def build_prompt(question: str, chunks):

    context_parts = []

    for i, chunk in enumerate(chunks, start=1):

        context_parts.append(
            f"""
SOURCE {i}

Company: {chunk["ticker"]}
Filing: {chunk["filing_type"]}
Year: {chunk["filing_year"]}
Section: {chunk["section_type"]}

{chunk["chunk_text"]}
"""
        )

    context = "\n\n".join(context_parts)

    prompt = f"""
You are an AI equity research assistant.

Answer the user's question using ONLY the supplied SEC filing excerpts.

Rules:

1. Prioritize the most recent filing when answering questions
   that do not specify a year.

2. Do not invent facts or figures.

3. Do not make causal claims unless the source explicitly
   supports the causal relationship.

4. Clearly distinguish between:
   - facts stated in the filing
   - reasonable interpretation

5. When numerical information is available, provide the
   exact figure and percentage change where appropriate.

6. When comparing historical periods, explicitly identify
   the years being compared.

7. If the supplied sources are insufficient to answer the
   question confidently, say so rather than speculating.

8. Cite sources using [Source 1], [Source 2], etc.

9. Prefer the most recent SEC filing unless the user asks
   about a specific historical period.

SEC FILING CONTEXT:

{context}

USER QUESTION:

{question}

Provide a clear, evidence-based answer.
"""

    return prompt
