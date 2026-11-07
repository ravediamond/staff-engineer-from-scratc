"""Self-contained. Run after predict.md."""
print("1. ~10 x 0.02 = 0.2 results on average (if relevance is independent of ACL): most queries return nothing")
c = 50_000 * 30 * (3000 * 3 + 300 * 15) / 1e6
print(f"2. ${c:,.0f}/month (input ${50_000 * 30 * 3000 * 3 / 1e6:,.0f}, output ${50_000 * 30 * 300 * 15 / 1e6:,.0f})")
print("3. fewer wrong answers, more 'I don't know'. Trust usually rises up to a point, then users stop asking. Pick it with data.")
