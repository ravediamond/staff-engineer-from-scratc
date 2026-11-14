"""Self-contained. Run after predict.md."""
import math

print(f"1. ceil(4 x 90/60) = {math.ceil(4 * 90 / 60)}")
print("2. 10: the ratio 0.95 is inside the 10% tolerance, no change.")
print("3. 10: scale-down uses the highest recommendation of the last 300 s.")
print("4. At most 12 pods; at least 9 available.")
print("5. Stalled: 2 new pods not Ready (surge), 9 old pods serving. Nothing is down; `kubectl rollout status` times out.")
print("6. The second eviction is refused (429) until the first replica is Ready again elsewhere: the drain waits.")
