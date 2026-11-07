"""Self-contained. Run after predict.md."""
import math
from statistics import NormalDist

p, n, z = 47 / 50, 50, 1.96
print(f"1. normal: upper {p + z * math.sqrt(p * (1 - p) / n):.3f} (can exceed 1 for p near 1); "
      f"Wilson: upper {((p + z * z / (2 * n)) + z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))) / (1 + z * z / n):.3f}")


def mcn(b, c):
    m = b + c
    k = min(b, c)
    return min(1.0, 2 * sum(math.comb(m, i) for i in range(k + 1)) / 2 ** m)


print(f"2. same pass counts can hide different discordance: b=30,c=30 -> p={mcn(30, 30):.2f}; b=40,c=20 -> p={mcn(40, 20):.3f}")
p1, p2 = 0.8, 0.85
za, zb = NormalDist().inv_cdf(0.975), NormalDist().inv_cdf(0.8)
pb = (p1 + p2) / 2
nn = (za * math.sqrt(2 * pb * (1 - pb)) + zb * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2 / (p1 - p2) ** 2
print(f"3. ~{math.ceil(nn)} cases per arm")
print("4. 20 x 0.05 = 1 expected false positive (64% chance of at least one)")
