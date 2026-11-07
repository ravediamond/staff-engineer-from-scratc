"""Self-contained. Run after predict.md."""
import math

print(f"1. sigma(1) = {1 / (1 + math.exp(-1)):.3f}")
print(f"2. 1 / (1 + 10^(-200/400)) = {1 / (1 + 10 ** (-0.5)):.3f}")
print("3. the likelihood keeps increasing as r_A -> infinity: no finite MLE. L2 (or a prior) keeps it finite.")
