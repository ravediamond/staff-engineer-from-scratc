"""Self-contained simulation of linear probing. Run after predict.md."""
import random

random.seed(0)


def avg_miss_probes(alpha, cap=10007, trials=2000):
    table = [False] * cap
    for _ in range(int(alpha * cap)):  # real linear-probing inserts: clusters form
        j = random.randrange(cap)
        while table[j]:
            j = (j + 1) % cap
        table[j] = True
    total = 0
    for _ in range(trials):
        j, n = random.randrange(cap), 1
        while table[j]:
            j, n = (j + 1) % cap, n + 1
        total += n
    return total / trials


for a in (0.5, 0.75, 0.9):
    print(f"1. alpha={a}: simulated {avg_miss_probes(a):.1f} probes, formula {0.5 * (1 + 1 / (1 - a) ** 2):.1f}")
print("   (primary clustering: occupied runs merge, so misses walk far longer than 1/(1-alpha))")

print("2. 1000 inserts, 900 deletes, no resize: tombstones keep the probe chains long, so misses stay as slow as at 1000 keys.")
print("   Fix: count tombstones in the load factor and rebuild.")
d = {1: "a", 1.0: "b", True: "c"}
print("3.", d, "-> keys equal AND same hash collapse to the first key object, last value wins")
d = {}
for k in ["z", "a", "m"]:
    d[k] = 1
print("4. iteration order:", list(d), "(insertion order, guaranteed since Python 3.7)")
print("5. multiples of 64 mod 64 -> distinct start slots:", len({(64 * i) % 64 for i in range(1000)}), "(why real hashes mix bits)")
