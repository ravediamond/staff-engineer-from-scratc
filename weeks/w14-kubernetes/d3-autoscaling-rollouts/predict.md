# Predict

1. 4 replicas at 90% CPU, target 60%. Desired replicas?
   Guess:

2. 10 replicas at 57% CPU, target 60%. Desired replicas?
   Guess:

3. Load drops; the HPA's raw recommendation goes 10, 4, 4, 4 over one minute. With the default scale-down stabilization, how many replicas after that minute?
   Guess:

4. replicas 10, maxSurge 2, maxUnavailable 1. Maximum pods during the rollout? Minimum available?
   Guess:

5. The new image crashes at start. With correct readiness probes, what is the state of the rollout an hour later?
   Guess:

6. 3 replicas, PDB minAvailable 2, all Ready. You drain two nodes that each host one replica, one after the other, without waiting. What happens to the second drain?
   Guess:

## Misses
-
