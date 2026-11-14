# W14 D4: GPU scheduling: gangs, quotas, claims, checkpoint interval

Primer: `knowledge/18-ml-platform-on-kubernetes.md` §1–3.

## The one idea

Kubernetes was built for services: schedule each pod alone, whenever it fits. Training breaks that.

**Gang scheduling.** A 4-worker job is useless with 3 workers. The default scheduler places pods one by
one, so two jobs can each hold half of the GPUs and wait for ever: a deadlock that burns money.
All-or-nothing admission fixes it: check that the WHOLE job fits, then place it, else place nothing.

**Quotas with borrowing (Kueue).** Each team has a `ClusterQueue` with a **nominal quota**. Queues in
the same **cohort** may **borrow** quota nobody is using. When the owner comes back, its workload
**reclaims** the quota by **preempting** borrowers. Result: high utilisation and a guarantee.
Kueue decides *whether* a job may start (admission); the scheduler still decides *where*.

**Devices.** A GPU is exposed either as a counter (`nvidia.com/gpu: 1`, the device plugin: any GPU
will do) or through **DRA** (Dynamic Resource Allocation, GA in Kubernetes 1.34): a `ResourceClaim`
selects devices by attributes ("at least 40 GB", "model H100"), like a PVC for hardware. Sharing one
GPU: **MIG** (hardware-isolated slices), **MPS** (concurrent, weak isolation), **time-slicing**
(no memory isolation: development only).

**Spot and checkpoints.** Training on preemptible nodes is 60–90% cheaper if you checkpoint. The
interval that minimises lost time (Young/Daly): `τ ≈ sqrt(2 × checkpoint_cost × MTBF)`.

## Today's build (`w14d4_gpu.py`)

`place_gang`, `QuotaManager.try_admit` / `release`, `match_devices`, `young_daly_interval`,
`wasted_fraction`.

## Staff angle

The interview question hiding here is "the cluster shows 40% GPU utilisation and teams complain they
cannot get GPUs: why?" Fragmentation (no whole node free), partial gangs, static per-team quotas with
no borrowing, and idle notebooks holding GPUs. Each has a mechanism in today's lab.
