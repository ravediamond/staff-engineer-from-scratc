"""Self-contained. Run after predict.md."""
po = 0.9
pe = 0.9 * 1.0 + 0.1 * 0.0
print(f"1. agreement {po:.0%}, kappa = ({po} - {pe}) / (1 - {pe}) = {(po - pe) / (1 - pe):.2f}")
po, pe = 0.8, 0.5
print(f"2. kappa = {(po - pe) / (1 - pe):.2f}")
print("3. consistent only when it picks first in one order and second in the other on the same pair.")
print("   With a 70% first-position preference and no real signal: P(consistent) = 2 x 0.7 x 0.3 = 0.42")
