"""Self-contained. Run after predict.md."""
import random

random.seed(0)
n = 200
base = [min(1, max(0, random.gauss(0.6, 0.3))) for _ in range(n)]
new = [min(1, b + 0.02) for b in base]


def boot(paired):
    ds = []
    for _ in range(2000):
        if paired:
            idx = [random.randrange(n) for _ in range(n)]
            ds.append(sum(new[i] - base[i] for i in idx) / n)
        else:
            a = [base[random.randrange(n)] for _ in range(n)]
            b = [new[random.randrange(n)] for _ in range(n)]
            ds.append(sum(b) / n - sum(a) / n)
    ds.sort()
    return ds[50], ds[1950]


print("1. unpaired CI:", [round(x, 3) for x in boot(False)], " paired CI:", [round(x, 3) for x in boot(True)])
print("2. single runs add noise of the same order as typical prompt effects -> rankings flip between runs; repeat or fix seeds")
print("3. 8% x -10 pts = -0.8 pt globally: invisible in the mean. Only slice gates catch it.")
