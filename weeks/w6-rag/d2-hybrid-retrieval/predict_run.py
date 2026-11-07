"""Self-contained. Run after predict.md."""
k = 60
a = 1 / (k + 1)
b = 1 / (k + 3) + 1 / (k + 3)
print(f"1. A = {a:.5f}, B = {b:.5f} -> {'B' if b > a else 'A'} wins: agreement across retrievers beats one top rank")
scores = [50, 5, 4.8, 4.5]
mn, mx = min(scores), max(scores)
print("2. normalised:", [round((s - mn) / (mx - mn), 3) for s in scores], "-> everything except the outlier is squashed near 0")
print("3. k=0: rank 1 gets 1.0, rank 2 gets 0.5: the top of any single list dominates. k=60 flattens, rewarding consensus.")
