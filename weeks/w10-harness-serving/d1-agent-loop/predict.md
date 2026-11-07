# Predict

1. A model emits `{"tool": "read_file", "args": {"pth": "a.txt"}}` (typo). What should the harness do?
   Guess:

2. max_steps = 5, model never produces a final answer. How many tool executions happen?
   Guess:

3. A tool raises `TimeoutError`. Crash the run, retry silently, or tell the model?
   Guess:

## Misses
-
