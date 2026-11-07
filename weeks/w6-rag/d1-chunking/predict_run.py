"""Self-contained. Run after predict.md."""
import math


def n_chunks(L, size, overlap):
    step = size - overlap
    return 1 if L <= size else math.ceil((L - size) / step) + 1


print("1.", n_chunks(10_000, 1000, 200), "chunks")
for ov in (0, 500):
    n = n_chunks(10_000, 1000, ov)
    print(f"2. overlap={ov}: {n} chunks, ~{n * 1000:,} chars stored ({n * 1000 / 10_000:.1f}x the source)")
per_doc = n_chunks(3000, 400, 50)
print(f"3. {per_doc} chunks/doc x 2M = {per_doc * 2e6:,.0f} embeddings")
