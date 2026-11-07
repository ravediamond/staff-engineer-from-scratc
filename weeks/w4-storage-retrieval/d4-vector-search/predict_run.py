"""Self-contained IVF experiment. Run after predict.md."""
import numpy as np

print(f"1. 10M x 768 x 4 bytes = {10e6 * 768 * 4 / 1e9:.1f} GB")
rng = np.random.default_rng(0)
centers = rng.normal(size=(50, 32))
X = centers[rng.integers(0, 50, 20000)] + 0.6 * rng.normal(size=(20000, 32))
X /= np.linalg.norm(X, axis=1, keepdims=True)
Q = X[rng.integers(0, 20000, 200)] + 0.1 * rng.normal(size=(200, 32))
Q /= np.linalg.norm(Q, axis=1, keepdims=True)
C = X[rng.choice(20000, 100, replace=False)].copy()
for _ in range(10):
    a = np.argmax(X @ C.T, axis=1)
    for j in range(100):
        if (a == j).any():
            C[j] = X[a == j].mean(0)
    C /= np.linalg.norm(C, axis=1, keepdims=True)
assign = np.argmax(X @ C.T, axis=1)
for nprobe in (1, 10):
    rec = []
    for q in Q:
        exact = set(np.argsort(-(X @ q))[:10])
        cells = np.argsort(-(C @ q))[:nprobe]
        cand = np.where(np.isin(assign, cells))[0]
        approx = set(cand[np.argsort(-(X[cand] @ q))[:10]])
        rec.append(len(exact & approx) / 10)
    print(f"{2 if nprobe == 1 else 3}. nprobe={nprobe}: scans ~{nprobe}% of vectors, recall@10 = {np.mean(rec):.2f}")
print("4. vectors with large norms (often long or boilerplate chunks) win regardless of direction.")
