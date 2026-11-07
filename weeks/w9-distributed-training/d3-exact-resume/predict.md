# Predict

1. You save model + optimizer but not RNG states. After resume, does the loss curve visibly change? Are the weights bitwise identical?
   Guess:

2. You forget the optimizer state with Adam. What do the first 10 steps after resume look like?
   Guess:

3. `torch.save(obj, path)` and the node dies halfway. What is at `path`?
   Guess:

## Misses
-
