"""Self-contained. Run after predict.md."""
print("1. curve looks similar (statistically equivalent), weights NOT bitwise identical: dropout masks and data order differ")
print("2. Adam's m and v restart at 0 with bias correction: effective steps are large and noisy -> a visible loss spike")
print("3. a truncated, unloadable file (and you overwrote the last good checkpoint). Always write tmp + os.replace.")
