"""Self-contained. Run after predict.md."""
import math

print(f"1. -log sigma(0) = log 2 = {math.log(2):.3f}")
print("2. beta multiplies the implicit reward; a larger beta saturates the sigmoid sooner -> smaller policy moves")
print("   (beta plays the role of the KL coefficient: larger = stay closer to the reference)")
s = [0.9, 0.95, 0.3, 0.9]
print(f"3. min {min(s)}, product {math.prod(s):.3f}, last {s[-1]} -> 'last' hides the broken step 3")
