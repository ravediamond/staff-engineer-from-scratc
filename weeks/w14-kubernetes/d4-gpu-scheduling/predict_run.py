"""Self-contained. Run after predict.md."""
import math

print("1. Deadlock: 16 GPUs held, neither job can start, and nothing will ever free a GPU. Gang scheduling prevents it.")
print("2. Yes: Y borrows 4 of X's idle quota. When X asks for 8, it reclaims: Y's borrowing workload is preempted.")
print("3. No: a pod runs on ONE node and no node has 4 free. Fragmentation. Bin-packing would have kept a node whole.")
print(f"4. sqrt(2 x 2 x 240) = {math.sqrt(2 * 2 * 240):.0f} minutes.")
print("5. 40 GB wanted on 24 GB: CUDA out-of-memory for whoever comes last. Time-slicing shares time, not memory. Use MIG for isolation.")
