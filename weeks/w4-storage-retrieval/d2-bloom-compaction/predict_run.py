"""Self-contained. Run after predict.md."""
import math

n, p = 1_000_000, 0.01
m = -n * math.log(p) / math.log(2) ** 2
k = m / n * math.log(2)
print(f"1. m = {m:,.0f} bits = {m / 8 / 1e6:.2f} MB, k = {k:.1f}")


def fp(m, n, k):
    return (1 - math.exp(-k * n / m)) ** k


print(f"2. k=1: {fp(m, n, 1):.3%} vs k=7: {fp(m, n, 7):.3%}")
print(f"3. 3x overfilled: {fp(m, 3 * n, 7):.1%}")
