"""Self-contained. Run after predict.md."""
import math

x, y = [1, 2, 3, 4, 5], [1, 3, 2, 4, 5]
c = d = 0
for i in range(5):
    for j in range(i + 1, 5):
        s = (x[i] - x[j]) * (y[i] - y[j])
        c += s > 0
        d += s < 0
print(f"1. concordant {c}, discordant {d}, tau = {(c - d) / 10:.2f}")
p = 2 * sum(math.comb(20, k) for k in range(13, 21)) / 2 ** 20
print(f"2. 13/20 sign agreement: two-sided p = {p:.2f} -> not distinguishable from a coin flip with 20 launches")
