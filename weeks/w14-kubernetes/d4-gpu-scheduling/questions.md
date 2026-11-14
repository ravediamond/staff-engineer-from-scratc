# Questions

1. Why does distributed training need gang scheduling, and where is it implemented (Kueue, Volcano, scheduler plugins)?
2. Explain Kueue's objects: ResourceFlavor, ClusterQueue, LocalQueue, cohort, borrowing, preemption. What does Kueue NOT do?
3. Device plugin vs DRA: what can a ResourceClaim express that `nvidia.com/gpu: 1` cannot?
4. MIG vs MPS vs time-slicing: isolation, use case, and what breaks.
5. "40% GPU utilisation, yet teams wait days for GPUs." Give five causes and the fix for each.
6. Training on spot GPUs: what must be true of the job, and how do you choose the checkpoint interval?

