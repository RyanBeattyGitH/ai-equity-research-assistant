from app.rag.rag_pipeline import ask_rag

question = "What are Apple's biggest financial risks?"

answer = ask_rag(question)

print("\n=== AI ANSWER ===\n")
print(answer)
