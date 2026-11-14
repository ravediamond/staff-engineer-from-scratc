"""Self-contained. Run after predict.md."""
import math

print("1. The order exists; no event was ever published. Inventory, billing and search never hear about it. Nothing retries.")
print("2. An event for an order that does not exist: consumers act on a phantom.")
print("3. The row is still unpublished: it is sent again. At-least-once -> consumers must deduplicate by event id.")
print("4. BACKWARD: no (a v2 reader has no value for `currency` in v1 data). FORWARD: yes (a v1 reader ignores the extra field).")
print(f"5. max(200/10, 200/5) x 1.5 = {math.ceil(max(200 / 10, 200 / 5) * 1.5)} partitions: the consumer is the bottleneck.")
