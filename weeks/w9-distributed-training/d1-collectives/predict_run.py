"""Self-contained. Run after predict.md."""
for n in (8, 64):
    print(f"{1 if n == 8 else 2}. N={n}: 2(N-1)/N x 1 GB = {2 * (n - 1) / n:.3f} GB per worker")
print("3. 63 GB into one server per step -> the server NIC is the bottleneck")
