"""Self-contained. Run after predict.md."""
import math
import random

rel, got = {"a", "b", "c"}, ["x", "a", "y", "b", "z"]
print(f"1. recall@5 = {2 / 3:.3f}, precision@5 = {2 / 5}, RR = 1/2")
dcg = sum(1 / math.log2(i + 2) for i, d in enumerate(got) if d in rel)
idcg = sum(1 / math.log2(i + 2) for i in range(3))
print(f"2. nDCG@5 = {dcg:.3f} / {idcg:.3f} = {dcg / idcg:.3f}")
random.seed(0)
per_q = [min(1, max(0, random.gauss(0.72, 0.3))) for _ in range(50)]
boots = sorted(sum(random.choices(per_q, k=50)) / 50 for _ in range(2000))
print(f"3. mean {sum(per_q) / 50:.2f}, 95% CI [{boots[50]:.2f}, {boots[1950]:.2f}] -> about +/-0.08 with 50 queries")
