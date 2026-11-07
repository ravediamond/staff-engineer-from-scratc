"""Self-contained. Run after predict.md."""
print("1. replica 2 never got the write -> stale (old value or nothing). R + W = 3 = N: no overlap guarantee.")
print("2. N=5, W=3: 2 failures for writes; R=3: 2 failures for reads.")
print("3. A's value survives: B's timestamp is 5 s lower even though it wrote later. LWW + clock skew = silent lost update.")
