"""Self-contained. Run after predict.md."""
print("1. capped bucket: 100 allowed instantly (tokens never exceed capacity). Uncapped bug: 36,000 + would be allowed.")
print("2. fixed window: 100 at 12:00:59 + 100 at 12:01:00 = 200 in ~1 s: the boundary burst.")
print(f"3. log: 1M keys x 10,000 timestamps x 8 bytes = {1e6 * 1e4 * 8 / 1e9:.0f} GB (worst case) -> why the counter approximation exists")
