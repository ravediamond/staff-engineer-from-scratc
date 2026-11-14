# Predict

1. A node has 8 CPUs; pods on it request 7 CPUs in total but use 1. Can a pod requesting 2 CPUs be scheduled there?
   Guess:

2. Pod: requests cpu 500m / memory 1Gi, limits cpu 500m / memory 2Gi. QoS class?
   Guess:

3. A container exceeds its CPU limit. And its memory limit. What happens in each case?
   Guess:

4. GPU nodes are tainted `gpu=true:NoSchedule`. A training pod has the toleration but no nodeSelector. Where can it land?
   Guess:

5. Two half-empty 8-GPU nodes, an 8-GPU job waiting. Which scoring strategy would have avoided this?
   Guess:

## Misses
-
