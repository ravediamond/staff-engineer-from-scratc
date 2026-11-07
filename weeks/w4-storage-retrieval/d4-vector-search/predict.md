# Predict

1. 10M vectors × 768 dims float32. Memory for the raw vectors?
   Guess:

2. IVF with nlist=100, nprobe=1. Fraction of vectors scanned per query, and expected recall@10 on clustered data: ~30%, ~70%, ~99%?
   Guess:

3. Same with nprobe=10?
   Guess:

4. Unnormalised vectors, dot product used as "cosine". Which documents dominate the results?
   Guess:

## Misses
-
