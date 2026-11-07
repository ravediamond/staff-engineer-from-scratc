"""Self-contained. Run after predict.md."""
import math

avg = 100e6 * 20 / 86400
print(f"1. avg {avg:,.0f} QPS (~23k), peak x3 {3 * avg:,.0f}")
s = 50e6 * 2e6 * 3 * 365 * 5
print(f"2. {s / 1e15:.0f} PB")
print(f"3. {20e3 * 50e3 * 8 / 1e9:.0f} Gbps")
g = 30 * (2000 / 20000 + 400 / 2000)
print(f"4. {g:.1f} GPU-seconds per second -> {math.ceil(g)} GPUs before headroom (decode dominates: 0.2 vs 0.1)")
print(f"5. 8 x 2.5 x 730 h = ${8 * 2.5 * 730:,.0f}/month")
