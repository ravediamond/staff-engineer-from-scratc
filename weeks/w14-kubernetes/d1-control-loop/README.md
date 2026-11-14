# W14 D1: the control loop

Primer: `knowledge/17-kubernetes.md` §1–2.

## The one idea

Kubernetes is a database with loops around it. The **API server** stores objects (in etcd): each has a
**spec** (what you want) and a **status** (what is). **Controllers** watch objects and act until status
matches spec. `kubectl apply` only writes the spec; everything after is a chain of controllers:

```
Deployment controller -> creates/updates a ReplicaSet
ReplicaSet controller -> creates Pods (no node yet)
Scheduler             -> writes spec.nodeName on each Pod
Kubelet on that node  -> pulls the image, starts containers, reports status
EndpointSlice ctrl    -> adds ready Pod IPs behind the Service
```

A controller's core is `reconcile(key)`: **read the current state, compare with desired, act**. It must be

- **level-triggered**: it acts on the state it reads now, not on the event that woke it. Events are
  only hints that something changed. They can be lost, duplicated, or arrive late.
- **idempotent**: running it twice in a row changes nothing the second time.

Events put a **key** in a **work queue**; the queue deduplicates, so ten events for one object cause
one reconcile.

## Today's build (`w14d1_reconcile.py`)

`WorkQueue`, `reconcile_replicaset(store, name)`. `Store` (a toy API server) is provided.

## Staff angle

This pattern is how you extend the platform: an **operator** is a custom resource (`ModelDeployment`,
`TrainJob`) plus a controller with this exact loop. When someone proposes a script that "creates the
GPU job when the request arrives", the staff answer is: make it a resource with a reconcile loop, so a
crash in the middle heals instead of leaking half-created jobs.
