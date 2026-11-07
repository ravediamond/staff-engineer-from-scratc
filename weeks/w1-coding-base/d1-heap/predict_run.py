"""Run after writing your guesses in predict.md. Self-contained: does not use your code."""
import heapq
import random

random.seed(0)


class Counted(float):
    n = 0

    def __lt__(self, other):
        Counted.n += 1
        return float.__lt__(self, other)


# 1
h = []
for x in [5, 3, 8, 1]:
    heapq.heappush(h, x)
print("1. array after pushes 5,3,8,1:", h)

# 2
data = [Counted(random.random()) for _ in range(1_000_000)]
Counted.n = 0
heapq.heapify(data)
print(f"2. heapify comparisons: {Counted.n:,}  ({Counted.n / 1e6:.2f} per item)")

# 3
data = [Counted(random.random()) for _ in range(1_000_000)]
Counted.n = 0
h = []
for x in data:
    heapq.heappush(h, x)
print(f"3. successive pushes comparisons: {Counted.n:,}  (random order is kind: most pushes stop after ~1-2 levels)")
data_sorted = sorted(float(x) for x in data)
Counted.n = 0
h = []
for x in reversed(data_sorted):  # worst case: decreasing input, every push sifts to the root
    heapq.heappush(h, Counted(x))
print(f"   worst case (decreasing input) pushes: {Counted.n:,}  vs heapify on same: ", end="")
arr = [Counted(x) for x in reversed(data_sorted)]
Counted.n = 0
heapq.heapify(arr)
print(f"{Counted.n:,}")

# 4
k, entered, h = 10, 0, []
for _ in range(1_000_000):
    x = random.random()
    if len(h) < k:
        heapq.heappush(h, x)
        entered += 1
    elif x > h[0]:
        heapq.heapreplace(h, x)
        entered += 1
print(f"4. items that entered the top-10 heap: {entered}  (theory: k * (1 + ln(n/k)) = {k * (1 + __import__('math').log(1e6 / k)):.0f})")

# 5
mh = []
for s, name in [(3, "c"), (9, "a"), (5, "b")]:
    heapq.heappush(mh, (-s, name))
print("5. push (-score, name); pop order:", [(-s, n) for s, n in [heapq.heappop(mh) for _ in range(3)]])
