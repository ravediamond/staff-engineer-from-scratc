"""Self-contained. Run after predict.md."""
import math

print(f"1. ceil(log2(1000)) = {math.ceil(math.log2(1000))} checks")
p1 = 1 - 0.8 ** 10
print(f"2. at most ~{p1:.0%} (each 'good' verdict can flip with p = 0.2; worst case all 10 checks land on good commits)")
p_wrong = sum(math.comb(5, k) * 0.2 ** k * 0.8 ** (5 - k) for k in range(3, 6))
print(f"3. per-check error with majority of 5: {p_wrong:.3f}; over 10 checks: {1 - (1 - p_wrong) ** 10:.1%}")
