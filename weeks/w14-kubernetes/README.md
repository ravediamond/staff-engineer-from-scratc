# Week 14: Kubernetes for ML platforms

**Everything you need for this week is on this page.** You need week 5 (job queues), week 9 (checkpoints) and week 10 day 4 (KV-cache arithmetic). You do not need to have used Kubernetes: this page starts from zero. Plain Python; nothing to install for the labs.

"How would you host and fine-tune models on Kubernetes?" is the other question you said went badly. Kubernetes looks like a thousand objects and commands. Underneath it is one idea repeated: you declare what you want, and loops work until reality matches. This week you build those loops (a controller, the scheduler, the autoscaler), then the parts that ML adds on top (jobs that need all their GPUs or none, quotas, model serving), then reproduce them on a real cluster on your Mac.

## Start here

1. Read [The week in one table](#the-week-in-one-table) and [Kubernetes in ten minutes](#kubernetes-in-ten-minutes).
2. Each day, open that day's folder and follow [What to do each day](#what-to-do-each-day).
3. The lesson for each day is the matching section of this page: [Day 1](#day-1-the-control-loop), [Day 2](#day-2-the-scheduler), [Day 3](#day-3-autoscaling-rolling-updates-disruption-budgets), [Day 4](#day-4-gpu-scheduling), [Day 5](#day-5-serving-an-llm-on-kubernetes-then-a-design).
4. Friday: [End of the week](#end-of-the-week).

### What is in a day folder

| File | What it is | You |
|---|---|---|
| `predict.md` | small questions, answered before you read anything | write guesses |
| `README.md` | one-page summary of the day, with its "staff angle" | read after the lesson |
| `predict_run.py` | prints the real answers | run, compare |
| `w14dN_*.py` | **the exercise**, with `# TODO` | **write the code** |
| `test_w14dN_*.py` | tests | run, never edit |
| `review_w14dN.py` + its test | code with one planted bug | **find and fix**, write the `WHY:` line |
| `questions.md` | interview questions | answer out loud |

Friday's folder also has `design.md` (the prompt) and `rubric.md`. You write your answer in a new file, `my_design.md`. After Wednesday's and Thursday's labs, do the hands-on track in `handson/k8s/` (three sessions of one hour, on a real cluster with `kind`).

### What to do each day

One hour, commands from the repo root.

| Min | Step | Command or file |
|---|---|---|
| 0–5 | Retrieve (Monday: 10-min delayed recall of last week's hardest function instead) | `uv run python scripts/review.py` |
| 5–10 | Guess, before reading | `predict.md` |
| 10–18 | Read the lesson | the day's section on this page |
| 18–20 | Check your guesses | `uv run python weeks/w14-kubernetes/<day>/predict_run.py` |
| 20–45 | Build, narrating out loud | `uv run pytest weeks/w14-kubernetes/<day> -k "not review"` until green |
| 45–53 | Review | `uv run pytest weeks/w14-kubernetes/<day> -k review` |
| 53–60 | Explain | `questions.md` out loud, then `uv run python scripts/review.py add weeks/w14-kubernetes/<day>` |

Guess before reading even if you know nothing: a wrong guess makes the lesson stick (`LEARNING.md` rule 1). AI stays off in the exercise files; stuck for 10 minutes, ask for a hint, not code.

## The week in one table

| Day | Folder | The question | You build | The review bug is about |
|---|---|---|---|---|
| Mon | `d1-control-loop` | how does Kubernetes do anything? | a work queue and a controller's reconcile function | what a controller reacts to |
| Tue | `d2-scheduler` | which machine runs my pod? | filter, score, bind; QoS classes; eviction order | what "room on a node" means |
| Wed | `d3-autoscaling-rollouts` | how do pod counts change safely? | the autoscaler formula, a rolling update step, a drain plan | which pods count as available |
| Thu | `d4-gpu-scheduling` | what does training need that services do not? | gang placement, quotas with borrowing, device claims, checkpoint interval | how a multi-pod job is placed |
| Fri | `d5-llm-serving-design` | how do you serve an LLM on it? | concurrency, cold start, cost, an endpoint picker, autoscaling; then a timed design | the signal used for autoscaling |

## Kubernetes in ten minutes

### What it is for

You have programs packaged as **containers** (a program with everything it needs, isolated from the others) and a fleet of machines. **Kubernetes** decides which machine runs what, restarts what crashes, replaces machines that die, and connects everything on the network. You describe the result you want; it keeps it true.

### The objects you must know

| Object | What it is |
|---|---|
| **node** | one machine (physical or virtual) of the cluster |
| **pod** | the smallest unit that runs: one or a few containers that share a network address. Pods are disposable: they are replaced, never repaired |
| **Deployment** | "keep N identical pods of this version running". It manages updates |
| **ReplicaSet** | the object a Deployment uses underneath to keep N pods alive |
| **Service** | a stable name and address in front of a changing set of pods |
| **namespace** | a named partition of the cluster, usually one per team or environment |
| **label** | a key-value tag on any object; other objects select things by label |
| **kubelet** | the agent on each node that actually starts and watches containers |
| **API server** | the front door: every read and write of any object goes through it |
| **etcd** | the database behind the API server. It uses Raft (week 3) |

### Spec and status

Every object has two parts: the **spec**, what you want, and the **status**, what currently is.

```yaml
kind: Deployment
spec:
  replicas: 3          # what I want
status:
  readyReplicas: 2     # what is true right now
```

`kubectl apply` writes a spec and does nothing else. Everything that happens afterwards is done by **controllers**: programs that watch objects and act until status matches spec. This model is called **declarative**: you state the destination, not the steps.

### What happens when you ask for 3 pods

```
you: kubectl apply (Deployment, replicas: 3)
Deployment controller → creates a ReplicaSet
ReplicaSet controller → creates 3 Pods, with no node yet
Scheduler             → picks a node for each Pod
Kubelet on each node  → pulls the image, starts the containers, reports status
Endpoint controller   → puts the ready Pods behind the Service
```

Five independent loops, each reading and writing objects through the API server, none calling another. Kubernetes is **a database with loops around it**. Hold on to that sentence and the rest of the week is detail.

## Day 1: The control loop

Folder: `d1-control-loop`. Exercise: `w14d1_reconcile.py`.

### Reconcile

The core of every controller is one function:

```
reconcile(key):  read the current state → compare with the desired state → act to reduce the difference
```

For a ReplicaSet that wants 3 pods: list the pods it owns. Two exist: create one. Five exist: delete two. Three exist: do nothing.

### Level-triggered, not edge-triggered

A controller is woken by **events**: "a pod was deleted". The tempting design reacts to the event itself: one deletion seen, so create one pod. That is **edge-triggered**, and it is wrong, because events are unreliable. One can be lost while the controller restarts. One can be delivered twice. Ten can arrive in a burst.

A correct controller is **level-triggered**: the event is only a hint that something changed. The controller then reads the **whole current state** and computes what to do from that. A lost event is repaired at the next reconcile; a duplicate causes a second reconcile that finds nothing to do.

Reacting to the events themselves is today's review bug. With one lost "pod deleted" event, an edge-triggered controller stays one pod short forever.

### Idempotent

Run reconcile twice in a row: the second run changes nothing. This follows from computing actions from the current state. It is what makes it safe to call reconcile any number of times, for any reason, including "just in case, every few minutes".

### The work queue

Events do not call reconcile directly. They put the **key** of the object (its name) in a **work queue**. The queue **deduplicates**: a key already waiting is not added again. Ten events for one object cause one reconcile.

### Ownership

A controller only touches what it **owns**. Each pod records its owner; the ReplicaSet controller lists the pods whose owner is this ReplicaSet and ignores all the others. When the owner itself is gone, what it owned is cleaned up.

### Traps of the day

- Acting on the event instead of the state.
- A second reconcile that creates more pods.
- Pods of another owner counted or deleted.
- A queue that holds the same key ten times.

### Today's build

| Piece | Job | Lesson section |
|---|---|---|
| `WorkQueue` | first-in first-out queue of keys, deduplicated | the work queue |
| `reconcile_replicaset` | make the owned pods match the spec; report what was created and deleted | reconcile; level-triggered; ownership |

`Store`, a toy API server, is provided.

Run: `uv run pytest weeks/w14-kubernetes/d1-control-loop -k "not review"`

---

## Day 2: The scheduler

Folder: `d2-scheduler`. Exercise: `w14d2_scheduler.py`.

### One pod at a time, two phases

The scheduler takes a pod that has no node and chooses one.

**Phase 1, filter**: remove the nodes where the pod **cannot** run.

- **Resources**: the node must have enough **unreserved** CPU and memory for what the pod **requests**.
- **Node selector**: every label the pod asks for must be on the node (`gpu: a100`).
- **Taints and tolerations**: a **taint** on a node repels pods. Only a pod that declares a matching **toleration** may land there.

**Phase 2, score**: rank the remaining nodes and **bind** the pod to the best one. Two opposite strategies:

| Strategy | Prefers | Why |
|---|---|---|
| **spread** (the default) | the emptiest node | resilience and headroom |
| **bin-pack** | the fullest node that still fits | fewer nodes to pay for; whole nodes stay free for large jobs |

For GPU clusters bin-packing matters: spread four small jobs over four 8-GPU nodes and no node can take an 8-GPU job any more, although half the GPUs are free.

### Requests and limits

Each container declares two numbers per resource:

- **request**: what it is guaranteed. **The scheduler uses only this.** It never looks at real usage.
- **limit**: the most it may use. Enforced later, on the node. CPU above the limit is **throttled** (the container slows down). Memory above the limit is an **OOM kill** (the container is killed).

The room left on a node is `capacity − the sum of the requests of the pods already placed there`. It is not the capacity, and it is not what is idle right now. Checking a new pod against the node's **capacity** ignores everything already placed, and puts ten pods on a node that has room for two. That is today's review bug.

### Dedicating nodes: you need both halves

A taint keeps other pods **off** a node. A node selector (or affinity) pulls a pod **to** a kind of node. To reserve GPU nodes for GPU workloads you need both: the taint so that web pods do not land on expensive GPU nodes, and the selector so that GPU pods do not land elsewhere.

### QoS classes: who is evicted first

When a node runs out of memory, the kubelet evicts pods. The order comes from a class computed from requests and limits:

| Class | Condition | Under memory pressure |
|---|---|---|
| **Guaranteed** | every container has request = limit, for CPU and memory | evicted last |
| **Burstable** | some request or limit is set, and it is not Guaranteed | in between |
| **BestEffort** | no request and no limit at all | evicted first |

Within that, pods using **more than their request** go before pods that stay within it. The practical rule for anything that matters, model servers included: set the memory request equal to the limit.

### Traps of the day

- A fit check against capacity.
- Scheduling by current usage.
- A taint with no toleration check, or a toleration read as an attraction.
- A pod with only limits classed as BestEffort: a missing request defaults to the limit.

### Today's build

| Function | Job | Lesson section |
|---|---|---|
| `filter_nodes` | nodes where the pod may run | phase 1 |
| `score` | spread or bin-pack score of a node | phase 2 |
| `schedule` | filter, score, bind, and reserve the requests | one pod at a time; requests and limits |
| `qos_class` | Guaranteed, Burstable or BestEffort | QoS classes |
| `eviction_order` | who goes first under memory pressure | QoS classes |

Run: `uv run pytest weeks/w14-kubernetes/d2-scheduler -k "not review"`

---

## Day 3: Autoscaling, rolling updates, disruption budgets

Folder: `d3-autoscaling-rollouts`. Exercise: `w14d3_rollout.py`.

Three loops change how many pods you have. Each has one formula.

### The Horizontal Pod Autoscaler (HPA)

Every 15 seconds:

```
desired = ceil( current replicas × current metric / target metric )
```

10 replicas at 90% CPU with a target of 60%: `ceil(10 × 90/60) = 15`.

Three guards:

- **Tolerance**: if the ratio is within 10% of 1, change nothing. Otherwise the count would twitch at every reading.
- **Bounds**: a minimum and a maximum number of replicas.
- **Stabilisation on the way down**: the autoscaler remembers its recommendations over a window (300 seconds by default) and applies the **highest** of them. So it scales **up at once** and **down slowly**: a short dip in traffic does not remove capacity that the next spike needs.

The metric can be CPU, or anything else through custom metrics: queue length, Kafka lag (with KEDA).

### Rolling updates

Replace version 1 by version 2 with no downtime, a few pods at a time. Two numbers bound the process:

- `maxSurge`: how many pods **above** the desired count may exist during the rollout;
- `maxUnavailable`: how many **below** the desired count may be unavailable.

With 10 replicas, `maxSurge = 2` and `maxUnavailable = 1`: never more than 12 pods in total, never fewer than 9 available.

**Only Ready pods are available.** A pod is **Ready** when its **readiness probe** passes: a check you define that says "I can take traffic". A new pod that has started and is still loading is not Ready.

That one rule is the safety catch of every deployment. If version 2 never becomes Ready, the rollout stops: old pods are not removed, because removing them would go below the minimum available. The broken version sits there, harmless, while version 1 keeps serving.

Count unready new pods as available, and the rollout deletes working old pods to make room for new pods that serve nothing. The service goes down during a "zero-downtime" deploy. That is today's review bug.

### PodDisruptionBudget (PDB)

Nodes are emptied (**drained**) for upgrades, repairs or cost. A PDB says "for this application, at least `minAvailable` pods must stay Ready". A drain removes pods through an API that **refuses** an eviction that would break the budget; the drain then waits.

A PDB protects against **voluntary** disruptions only. It does nothing when a node crashes.

### After today's lab: the real thing

`handson/k8s/README.md`, core sessions: a real cluster on your Mac with `kind`. You deploy, break a readiness probe and watch a rollout stall, drain a node against a PDB, and watch controllers recreate pods you delete. Write what you saw in the day's `questions.md`. The guide states honestly that its commands were written from the documentation and not executed when the repo was generated; when one fails, fixing it is part of the exercise, and asking for help there is allowed.

### Traps of the day

- Unready pods counted as available.
- No tolerance, or stabilisation applied on the way up.
- The lowest recommendation of the window in place of the highest.
- A PDB expected to survive a node crash.

### Today's build

| Piece | Job | Lesson section |
|---|---|---|
| `hpa_desired` | the formula with tolerance and bounds | the HPA |
| `Stabilizer` | the highest recommendation of the window | the HPA |
| `rollout_step` | how many new pods to create and old pods to delete, within surge and unavailable | rolling updates |
| `drain_plan` | which pods of a node may be evicted now, given the budgets | PodDisruptionBudget |

Run: `uv run pytest weeks/w14-kubernetes/d3-autoscaling-rollouts -k "not review"`

---

## Day 4: GPU scheduling

Folder: `d4-gpu-scheduling`. Exercise: `w14d4_gpu.py`.

Kubernetes was built for services: place each pod alone, whenever it fits. Training breaks that assumption in four ways.

### Gang scheduling

A training job with 4 workers is useless with 3: it cannot start. The default scheduler places pods one by one. Two jobs can each get half of the GPUs and wait forever for the other half: a **deadlock** that burns money on GPUs doing nothing.

The fix is **all-or-nothing** admission: check that the **whole** job fits, and only then place it. If it does not fit, place **nothing** and leave the GPUs free for a job that does.

In a simulation, that means trying the placement on a **copy** of the free capacity and committing only if every pod found a place. Reserving pod by pod and stopping halfway leaves GPUs held by a job that will never run. That is today's review bug.

### Quotas with borrowing

Several teams share a cluster. Fixed shares waste capacity: team A's GPUs sit idle at night while team B queues. **Kueue**, the standard Kubernetes add-on for batch workloads, uses quotas with borrowing:

- each team's queue has a **nominal quota**: what it is guaranteed;
- queues in the same **cohort** may **borrow** quota that nobody is using;
- when the owner comes back, its workload **reclaims** the quota by **preempting** the borrowers.

High utilisation **and** a guarantee. The catch is that borrowed capacity can be taken back at any time, so jobs that borrow must checkpoint (week 9).

Kueue decides **whether** a job may start (admission). The scheduler still decides **where** its pods go. Two separate questions, two separate components.

### Asking for a GPU

Two ways to expose devices:

- **A counter**: `nvidia.com/gpu: 1`. "Any GPU will do."
- **A claim** (Dynamic Resource Allocation): a request that selects devices by attributes, such as "at least 40 GB of memory, model H100". Among the devices that match, pick the **smallest that fits**, so that large ones stay free for requests that need them.

Sharing one GPU among workloads: **MIG** (hardware slices, isolated), **MPS** (concurrent use, weak isolation), **time-slicing** (no memory isolation; development only).

### Spot nodes and the checkpoint interval

Preemptible (**spot**) machines cost 60 to 90% less and can disappear at any moment. Training on them works if you checkpoint. How often?

- Checkpoint too often: time is lost writing checkpoints.
- Too rarely: each failure loses a lot of work.

The interval that minimises the total loss (the Young/Daly formula), with `C` the time to write a checkpoint and `MTBF` the mean time between failures:

```
τ ≈ sqrt( 2 × C × MTBF )

fraction of time lost ≈ C / τ  +  τ / (2 × MTBF)
                        writing    redoing: on average half an interval per failure
```

A checkpoint of 1 minute and a failure every 8 hours: `τ = sqrt(2 × 1 × 480) ≈ 31` minutes, and about 6.5% of the time is lost.

### After today's lab

`handson/k8s/README.md`, the queues session: Kueue on your cluster, two queues that borrow from each other, and a preemption.

### Traps of the day

- A gang reserved pod by pod.
- The largest matching device given to a small request.
- Borrowing with no preemption when the owner returns.
- `C` and `MTBF` in different time units.

### Today's build

| Piece | Job | Lesson section |
|---|---|---|
| `place_gang` | all pods of a job, or none | gang scheduling |
| `QuotaManager` | admit within the nominal quota, by borrowing, or by preempting borrowers; release | quotas with borrowing |
| `match_devices` | devices that satisfy a claim, smallest first | asking for a GPU |
| `young_daly_interval`, `wasted_fraction` | the best interval and the time lost | spot nodes |

Run: `uv run pytest weeks/w14-kubernetes/d4-gpu-scheduling -k "not review"`

---

## Day 5: Serving an LLM on Kubernetes; then a design

Folder: `d5-llm-serving-design`. Exercise: `w14d5_serving.py`. Also in the folder: `design.md`, `rubric.md`.

An LLM server is not a web server. Four facts change the design of the platform.

### 1. Memory caps concurrency

Each sequence being generated holds a **KV cache** (week 10, day 4): `2 × layers × KV heads × head dimension × bytes per number` for every token.

```
concurrent sequences = floor( (GPU memory − weights − overhead) / (context length × KV bytes per token) )
```

It is the capacity of one replica, and the first number of any serving design. The docstring of today's function fixes the unit (here a GB is 2³⁰ bytes).

### 2. A cold start takes minutes

A new replica needs: a node (if none is free), the container image (10 GB), the model weights (16 to 140 GB), and the load of those weights into the GPU. Each step is skipped if already done: a node that is up, an image already on it, weights cached on a local disk.

You cannot autoscale your way out of a traffic spike in seconds. So: warm replicas, headroom, images and weights pre-loaded on nodes.

### 3. GPU utilisation says nothing

For a web server, CPU utilisation tracks load, and the autoscaler of Wednesday uses it. With continuous batching, a GPU shows about 100% utilisation with **one** request and with **fifty**. The number does not move with load.

An autoscaler that follows it either never adds replicas, or adds them forever. Scale on a signal that does follow load: **queue depth**, KV-cache usage, or time to first token. Autoscaling on GPU utilisation is today's review bug, and one of the most common real mistakes on ML platforms. The provided `simulate` lets you run both signals through the same traffic and see the difference.

### 4. Replicas are not interchangeable

Behind a web service, any pod can answer any request, so round-robin is fine. LLM replicas hold state that matters: one has your long prompt prefix already in its cache (the answer starts faster and costs less); another has your LoRA adapter loaded. Round-robin throws that away.

An **inference-aware gateway** picks the replica for each request with a score that weighs: does it have this prefix cached, does it have this adapter loaded, how long is its queue. Replicas whose KV cache is nearly full are skipped, unless all of them are.

### The cost number

```
cost per million tokens = price per GPU-hour / ( tokens per second × 3600 × utilisation ) × 1 000 000
```

A GPU that is busy half the time costs twice as much per token. That is why batching, routing and right-sized autoscaling are money, and why this number belongs in every design.

### After the lab: the Friday design (45 minutes, timed)

`design.md` is design number 8: host and fine-tune LLMs on Kubernetes. It is the question you want to be good at.

1. Start a 45-minute timer. Write in `my_design.md`, following the 45-minute frame of [week 5](../w5-design-method/README.md#the-45-minute-frame). Stop at the bell.
2. Grade yourself with `rubric.md`.
3. Only then read the model answer: `model_answer.md`, in the same folder on the `solutions` branch.
4. Write in `PROGRESS.md` the one thing that would have raised your level.

A skeleton of what a strong answer touches, all from this week and weeks 9 and 10: separate node pools for serving and training, with taints; requests equal to limits for model servers; Kueue with quotas and borrowing for training, gang admission; spot nodes with checkpoints for fine-tuning; serving capacity from the KV arithmetic; cold-start mitigation; autoscaling on queue depth; an inference-aware gateway; readiness probes that wait for the weights; rollouts with surge; and the cost per million tokens.

### Traps of the day

- Autoscaling on GPU utilisation.
- Concurrency computed without subtracting the weights.
- Cold start counted as seconds.
- Round-robin in front of replicas with caches and adapters.

### Today's build

| Function | Job | Lesson section |
|---|---|---|
| `kv_bytes_per_token`, `max_concurrency` | capacity of one replica | fact 1 |
| `cold_start_seconds` | time until a new replica can serve | fact 2 |
| `cost_per_million_tokens` | dollars per million tokens | the cost number |
| `pick_endpoint` | the best replica for a request | fact 4 |
| `desired_replicas` | the autoscaler formula on a chosen signal | fact 3 |

Run: `uv run pytest weeks/w14-kubernetes/d5-llm-serving-design -k "not review"`

---

## End of the week

- **AI-off gate (15 min):** redo one drill you marked slow in `PROGRESS.md`, from a blank file, timer on, AI fully off.
- **Ship one public thing** and log it in `SHIPLOG.md`: one claim, one piece of evidence. A write-up of this week's hardest lab with its numbers counts.
- **Tick `PROGRESS.md`**, write the retro, and name the hardest lab: next Monday you rewrite its main function from a blank file.

You are done with week 14 when you can do these without notes:

- [ ] say what happens, loop by loop, after `kubectl apply` of a Deployment
- [ ] explain level-triggered and idempotent reconciliation
- [ ] explain filter and score, requests against limits, taints with selectors, and the three QoS classes
- [ ] write the autoscaler formula; explain `maxSurge`, `maxUnavailable` and why readiness is the safety catch
- [ ] explain gang scheduling, quotas with borrowing and preemption, and the checkpoint interval formula
- [ ] give the four facts that make LLM serving different, and the signal to autoscale on
- [ ] describe what you saw when a rollout stalled on a real cluster

## Optional depth (not needed for the labs)

- Interview questions with short answers: `knowledge/17-kubernetes.md`, `knowledge/18-ml-platform-on-kubernetes.md`
- The real tool: `handson/k8s/README.md`
- Previous week: [`../w13-streaming/README.md`](../w13-streaming/README.md) · Next: [`../w15-databases/README.md`](../w15-databases/README.md)
