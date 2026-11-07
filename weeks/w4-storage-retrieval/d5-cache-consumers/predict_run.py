"""Self-contained. Run after predict.md."""
print("1. 10,000 req/s x 0.2 s = ~2,000 concurrent misses -> ~2,000 DB loads for one key (single-flight: 1)")
print("2. All expire together -> synchronized stampede every 300 s. Fix: TTL jitter (e.g. 300 s +/- 10%) + single-flight.")
print("3. ~100,000 messages lost silently (if a crash happens on 1% of messages).")
