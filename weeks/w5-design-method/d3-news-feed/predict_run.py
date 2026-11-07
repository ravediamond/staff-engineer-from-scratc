"""Self-contained. Run after predict.md."""
w = 300e6 * 200 / 86400
print(f"1. {w:,.0f} inbox writes/s average (~700k/s)")
c = 80e6 * 10 / 86400
print(f"2. celebrity alone: {c:,.0f}/s = {c / (w + c):.1%} of all writes, and in bursts of 80M at once")
print("3. inbox read + 30 outbox reads (cached, hot) + a 31-way merge of short lists: cheap")
