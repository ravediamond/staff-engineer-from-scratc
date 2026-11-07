"""Self-contained. Run after predict.md."""
per_tok = 2 * 32 * 8 * 128 * 2
print(f"1. {per_tok / 1024:.0f} KB per token; 32k context = {per_tok * 32768 / 2 ** 30:.1f} GiB per sequence")
print(f"2. (80 - 16) GB / ({per_tok} B x 2048) = {64e9 / (per_tok * 2048):.0f} sequences")
print("3. static: only when the 500-token one finishes (step 500); continuous: at step 10")
