"""Self-contained. Run after predict.md."""
print("1. without a version check: version 3 (stale) wins -> silent data loss. With the check: version 4 stays.")
print("2. 30,000 wrong keys: not before understanding them (classify: encoding? deletes? races?). Threshold set in advance.")
print("3. instant rollback: reads can flip back to old with zero data loss while the new path proves itself")
