"""Self-contained. Run after predict.md."""
print(f"1. 16 x 7e9 = {16 * 7e9 / 1e9:.0f} GB per GPU (does not fit in 80 GB)")
print(f"2. 16 x 7e9 / 64 = {16 * 7e9 / 64 / 1e9:.2f} GB per GPU")
print(f"3. (80 - 20) GB / 16 bytes = {60e9 / 16 / 1e9:.2f} B parameters")
