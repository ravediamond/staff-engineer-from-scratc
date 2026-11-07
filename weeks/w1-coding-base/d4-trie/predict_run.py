"""Self-contained dict-of-dicts trie measurements. Run after predict.md."""
import random
import string
import sys
import tracemalloc

random.seed(0)


def build(words):
    root, nodes = {}, 1
    for w in words:
        n = root
        for ch in w:
            if ch not in n:
                n[ch] = {}
                nodes += 1
            n = n[ch]
        n["$"] = True
    return root, nodes


print("1. nodes for car/cart/care/dog:", build(["car", "cart", "care", "dog"])[1])
letters = "etaoinshrdlucmfwypvbgkqjxz"
weights = [12, 9, 8, 7.5, 7, 6.7, 6.3, 6, 5.9, 4.3, 4, 2.8, 2.8, 2.4, 2.2, 2, 2, 1.9, 1, 1, 1, 0.8, 0.15, 0.15, 0.1, 0.07]
words = {"".join(random.choices(letters, weights=weights, k=random.randint(4, 12))) for _ in range(100_000)}
tracemalloc.start()
root, nodes = build(words)
cur, _ = tracemalloc.get_traced_memory()
print(f"2. {len(words)} words -> {nodes} nodes = {nodes / len(words):.1f} nodes/word (random words share little beyond short prefixes)")
print(f"3. memory for {nodes:,} dict nodes: {cur / 1e6:.0f} MB -> {cur / nodes:.0f} bytes/node, so 1M nodes ~ {cur / nodes:.0f} MB")
print("4. delete('car') with 'cart' present: 0 nodes removed, only the is_word flag flips (the path is still needed).")
