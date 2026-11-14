"""Self-contained. Run after predict.md."""
print("1. The ReplicaSet controller creates Pods (the Deployment controller creates the ReplicaSet). The scheduler picks nodes.")
print("2. Yes: at its next reconcile (startup lists everything; periodic resync) it counts 2 pods, wants 3, creates 1.")
print("3. Two new pods: 4 instead of 3. Edge-triggered logic breaks under duplicate or lost events.")
print("4. One. The work queue holds keys, not events; duplicates collapse.")
print("5. The two not-ready ones: they serve nothing. (Then: unscheduled, newer, on fuller nodes...)")
