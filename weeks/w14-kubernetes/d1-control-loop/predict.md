# Predict

1. `kubectl apply` a Deployment with 3 replicas. Which component creates the Pod objects? Which one decides the node?
   Guess:

2. A ReplicaSet wants 3 pods. You delete one by hand. The controller misses the delete event (it was restarting). Is the pod replaced? When?
   Guess:

3. The same "pod deleted" event is delivered twice to a controller that does "on delete: create one pod". Result?
   Guess:

4. 10 events for the same ReplicaSet arrive while the controller is busy. How many reconciles should run for them?
   Guess:

5. Scale from 5 to 3. Two pods are not ready (crash-looping). Which pods should be deleted?
   Guess:

## Misses
-
