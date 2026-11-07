"""Self-contained. Run after predict.md."""
import math

print(f"1. log 2 = {math.log(2):.3f} (both rewards equal -> sigma(0) = 0.5)")
print("2. labels are noisy: when true rewards are close, BT gives the 'worse' answer a real chance of winning.")
print("   The Bayes-optimal accuracy is E[max(p, 1 - p)] over pairs, < 1.")
print("3. up, and not real: the test set shares prompts (and their features) with training -> leakage.")
