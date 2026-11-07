"""Self-contained. Run after predict.md."""
n = 62 ** 7
print(f"1. 62^7 = {n:.2e} codes -> {n / (100e6 * 12):,.0f} years at 100M/month")
print("2. sequence covers 4,096 per ms -> the rest wait for the next ms (throughput cap ~4M IDs/s per worker)")
print("3. the last 3 items of page 1 appear again at the top of page 2 (duplicates); deletes cause skips")
