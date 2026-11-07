"""Self-contained. Run after predict.md."""
print("1. At 60 s the job is re-leased to a second worker -> both run it; the first one's completion must be rejected (stale token).")
print("2. It cycles forever, burning a worker slot each time and starving others. DLQ after N attempts.")
print("3. priority 9 first, then the three priority-5 jobs in submission order (FIFO within priority).")
