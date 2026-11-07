"""Self-contained. Run after predict.md."""
import math
import random

print(f"1. log 16 - 15/16 = {math.log(16) - 15 / 16:.2f} nats")
rng = random.Random(0)
for n in (1, 4, 16, 64, 256):
    g = 0.0
    for _ in range(400):
        s = [(rng.gauss(0, 1), abs(rng.gauss(0, 1))) for _ in range(n)]
        q, l = max(s, key=lambda x: x[0] + 1.5 * x[1])
        g += q - 0.3 * l * l
    print(f"2. N={n:>3}: mean gold of the pick = {g / 400:+.2f}")
print("3. the judge selected AND scored the samples: winner's curse. Its errors are exactly what BoN found.")
