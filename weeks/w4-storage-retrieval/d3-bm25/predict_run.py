"""Self-contained. Run after predict.md."""
import math

N = 1000
print(f"1. df=N: IDF = ln(0.5/1000.5 + 1) = {math.log(0.5 / 1000.5 + 1):.5f} (tiny, never negative with the +1)")
k1 = 1.5


def sat(tf):
    return tf * (k1 + 1) / (tf + k1)


print(f"2. tf=10 vs tf=1: {sat(10) / sat(1):.2f}x (saturation)")
print("3. b=0: no length normalisation -> long documents win by sheer term count (keyword stuffing works).")
