"""Self-contained. Run after predict.md."""
import json

print("1.", json.dumps({"b": 1, "a": 2}), "vs", json.dumps({"a": 2, "b": 1}), "-> different strings, same object")
print("   canonical:", json.dumps({"b": 1, "a": 2}, sort_keys=True, separators=(",", ":")))
print("2. ~", int(1e6 * 0.02), "double charges (every timed-out-but-succeeded charge that is retried)")
print("3. PUT with full replacement: idempotent. increment: not idempotent (each call changes state).")
print("4. Both servers see 'absent', both execute -> double effect. Needs an atomic insert-if-absent (unique constraint, SETNX, conditional put).")
