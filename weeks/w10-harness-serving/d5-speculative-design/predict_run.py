"""Self-contained. Run after predict.md."""
a, k, c = 0.8, 4, 0.1
e = (1 - a ** (k + 1)) / (1 - a)
print(f"1. (1 - 0.8^5) / 0.2 = {e:.2f} tokens per target pass")
print(f"2. {e:.2f} / (1 + 4 x 0.1) = {e / (1 + k * c):.2f}x")
print("3. output distribution would follow the draft's confident guesses, not the target: quality changes silently")
