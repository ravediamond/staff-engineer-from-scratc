"""Self-contained. Run after predict.md."""
print("1. 10: the snapshot is fixed for the whole transaction (repeatable read).")
print("2. 20: each statement takes a new snapshot (non-repeatable read).")
print("3. T2 fails with a serialization failure (first committer wins) and must retry: it then reads 11 and writes 12.")
print("4. 11: one increment is lost. Fix: UPDATE x = x + 1, SELECT ... FOR UPDATE, or a stricter level with retries.")
print("5. Yes: write skew. Different rows were written, so no write-write conflict. Only serializable catches it.")
print("6. Dead row versions: VACUUM cannot remove anything newer than the oldest open snapshot. Bloat, slower scans.")
