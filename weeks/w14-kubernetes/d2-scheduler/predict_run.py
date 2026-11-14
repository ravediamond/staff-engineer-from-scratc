"""Self-contained. Run after predict.md."""
print("1. No. Scheduling uses requests: 7 + 2 > 8. Real usage is irrelevant to the scheduler.")
print("2. Burstable (memory request != limit). Guaranteed needs requests == limits for both resources in every container.")
print("3. CPU: throttled by the CFS quota (slower, latency spikes). Memory: the kernel OOM-kills the container (restart).")
print("4. Anywhere, CPU nodes included: a toleration only permits. Add a nodeSelector/affinity to attract it to GPU nodes.")
print("5. Bin-packing (MostAllocated): fill one node before opening the next, keeping whole nodes free for big jobs.")
