# Questions

1. What happens between `kubectl apply -f deployment.yaml` and a container running? Name each component and what it writes.
2. Level-triggered vs edge-triggered: define both and say why Kubernetes controllers are level-triggered.
3. What are informers, the local cache, the work queue and resync for?
4. What is an operator? Sketch the reconcile loop of a `ModelDeployment` operator (weights in object storage, N replicas on GPUs).
5. Two controllers fight over the same field (HPA and a GitOps tool both set `replicas`). What do you see and how do you fix it?
6. Why is etcd behind the API server a consensus system, and what happens to the cluster when etcd loses quorum?

