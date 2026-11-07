"""Self-contained. Run after predict.md."""
import math

print("1. lr x world size (2x): the update is the sum of two mean gradients")
print("2. ranks draw overlapping samples and miss others: the epoch is no longer a permutation of the data")
print(f"3. ceil(10/4) = {math.ceil(10 / 4)} each (2 samples duplicated to pad 10 -> 12)")
