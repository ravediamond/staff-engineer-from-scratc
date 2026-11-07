"""Self-contained. Run after predict.md."""
import random

print("1. a list whose sum is exactly 100 (greedy shrinking walks values down until the next step would pass)")
print("2. three equal adjacent values, e.g. [3, 3, 3]: the buggy version only skips one duplicate.")
print("   Greedy shrinking cannot lower them one at a time (two equal values pass), so the values stay where they were found.")
rng = random.Random(0)
hits = sum(any(a == b for a, b in zip(sorted(l), sorted(l)[1:]))
           for l in ([rng.randrange(100) for _ in range(rng.randint(0, 10))] for _ in range(200)))
print(f"3. {hits}/200 lists contain a duplicate after sorting; triples are rarer -> bias generators toward small ranges")
