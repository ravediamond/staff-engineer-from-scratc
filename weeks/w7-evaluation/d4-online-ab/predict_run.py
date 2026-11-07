"""Self-contained. Run after predict.md (~5 s)."""
import math
import random

na, nb = 50_600, 49_400
e = (na + nb) / 2
chi2 = (na - e) ** 2 / e + (nb - e) ** 2 / e
print(f"1. chi2 = {chi2:.1f}, p = {math.erfc(math.sqrt(chi2 / 2)):.5f} -> investigate before reading any metric")
print(f"2. 1 - rho^2 = {1 - 0.8 ** 2:.2f} -> variance reduced by {0.8 ** 2:.0%}")
random.seed(0)
fp = 0
for _ in range(1000):
    a = b = na_ = nb_ = 0
    for look in range(10):
        for _ in range(200):
            a += random.random() < 0.1
            b += random.random() < 0.1
        na_ += 200
        nb_ += 200
        p = (a + b) / (na_ + nb_)
        se = math.sqrt(p * (1 - p) * (2 / na_))
        if se > 0 and abs((b / nb_ - a / na_) / se) > 1.96:
            fp += 1
            break
print(f"3. false positive rate with 10 peeks: {fp / 1000:.1%} (nominal 5%)")
