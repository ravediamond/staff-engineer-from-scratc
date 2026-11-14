"""Self-contained. Run after predict.md."""
import math

print(f"1. log_200(1e9) = {math.log(1e9, 200):.1f} -> 4 levels; the top levels are always in memory.")
print("2. Leaf [1,2,3,4] overflows at 5: split into [1,2] and [3,4,5], new root with separator 3. Height 2.")
print("3. One (tenant_id). status comes after created_at in the index, so it only filters rows already scanned.")
print("4. Two: equality on tenant_id, range on created_at. status is again a filter, not a seek.")
print("5. No (no leftmost prefix): a full index or table scan. Needs its own index starting with created_at.")
print("6. Random keys insert all over the tree: every insert dirties a different page, pages split half-full, "
      "the cache is useless. Time-ordered keys append to the rightmost leaf.")
