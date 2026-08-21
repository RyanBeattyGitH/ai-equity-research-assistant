from app.rag.rag_pipeline import ask_rag


question = "What was Apple's total net sales in 2025, and how did this compare with 2024?"

result = ask_rag(
    question=question,
    ticker="AAPL",
)


print("\n" + "=" * 80)
print("ANSWER")
print("=" * 80)

print(result["answer"])


print("\n" + "=" * 80)
print("SOURCES")
print("=" * 80)

for i, source in enumerate(result["sources"], start=1):

    print(f"\nSOURCE {i}")
    print(f"Ticker: {source['ticker']}")
    print(f"Filing: {source['filing_type']}")
    print(f"Year: {source['filing_year']}")
    print(f"Section: {source['section_type']}")
    print(f"Distance: {source['distance']:.4f}")

    print("\nText:")
    print(source["text"][:500])

    print("-" * 80)
