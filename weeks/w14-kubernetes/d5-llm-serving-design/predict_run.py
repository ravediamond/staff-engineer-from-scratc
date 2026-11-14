"""Self-contained. Run after predict.md."""
kv = 2 * 32 * 8 * 128 * 2
print(f"1. 2 x 32 x 8 x 128 x 2 bytes = {kv:,} bytes = {kv // 1024} KiB per token")
seq_gb = 8192 * kv / 2**30
print(f"2. {seq_gb:.1f} GiB per 8k sequence -> ({80} - 16 - 4) / {seq_gb:.1f} = {int((80 - 20) / seq_gb)} sequences")
print(f"3. 180 + 12/0.2 + 140/1 + 140/2 = {180 + 60 + 140 + 70} s = 7.5 minutes")
c = 3 / (2000 * 3600) * 1e6
print(f"4. ${c:.2f} per 1M tokens at full load; ${c / 0.2:.2f} at 20% utilisation. Utilisation is the cost lever.")
print("5. GPU utilisation stays near 100% on any replica that is decoding anything. Queue depth drops to 0: the usable signal.")
