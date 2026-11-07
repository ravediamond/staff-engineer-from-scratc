"""Self-contained. Run after predict.md."""
import math

print(f"1. {50e6 / 100e3:.0f} gateways, {math.ceil(50e6 / 100e3 * 1.2)} with 20% headroom")
print(f"2. {50e6 / 30:,.0f} heartbeats/s -> batch them, keep presence in memory with TTL, publish only state changes")
p, q = 0, 0
for s in (5, 9, 7):
    p, q = max(p, s), s
    print(f"3. ack {s}: with max -> {p}, without -> {q}")
