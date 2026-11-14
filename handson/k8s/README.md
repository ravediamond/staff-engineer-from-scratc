# Hands-on Kubernetes (after W14 D3, then D4)

Not executed by the author of this repo (see `handson/README.md`). Docs: https://kubernetes.io/docs/ ·
https://kind.sigs.k8s.io/ · https://kueue.sigs.k8s.io/

```bash
kind create cluster --name staff --config handson/k8s/kind.yaml
kubectl get nodes -o wide
alias k=kubectl
```
Keep `k9s` or `watch kubectl get pods -o wide` open in a second terminal for every step.

## Session 1: the control loop and rollouts (W14 D1, D3)

1. `k create deployment web --image=nginx:1.27 --replicas=3`. Then find each link of the chain:
   `k get deploy,rs,pods -o wide`, `k describe pod <one>` (read the Events from bottom to top:
   Scheduled → Pulling → Created → Started), `k get events --sort-by=.lastTimestamp`.
2. Level-triggered: `k delete pod <one>` and watch the ReplicaSet replace it. `k scale deploy web --replicas=5`,
   then edit the ReplicaSet directly to 2 replicas: who wins, and why?
3. Rolling update: `k set image deploy/web nginx=nginx:1.28 && k rollout status deploy/web`.
   `k get rs` during the rollout: two ReplicaSets changing size. `k rollout history deploy/web`, `k rollout undo deploy/web`.
4. Broken release: `k set image deploy/web nginx=nginx:does-not-exist`. Predict the pod states and how
   many old pods keep serving (`maxSurge`/`maxUnavailable` default to 25%). Look, then `k rollout undo`.
5. Probes: add a readiness probe that fails (`httpGet` on a wrong path) with `k edit deploy web`.
   The pods are Running but not Ready: `k get endpointslices` shows no endpoints. That is how a bad
   deploy is kept out of traffic.
6. Requests, limits, OOM: run `k run hog --image=polinux/stress --restart=Never --limits=memory=64Mi -- stress --vm 1 --vm-bytes 128M`
   (if `--limits` is rejected by your kubectl, write the 15-line pod YAML). `k describe pod hog`: `OOMKilled`, exit code 137.
   Check its QoS class in the `describe` output; predict it first.
7. PDB and drain: `k create pdb web --selector=app=web --min-available=4` (with 5 replicas),
   then `k drain <a worker> --ignore-daemonsets`. Watch evictions go one at a time. Set `--min-available=5`
   and drain another node: it hangs. `k uncordon` both.
8. HPA: install metrics-server (on kind it needs the `--kubelet-insecure-tls` argument:
   https://github.com/kubernetes-sigs/metrics-server), give the deployment CPU requests,
   `k autoscale deploy web --cpu-percent=50 --min=2 --max=10`, generate load with a busybox `wget` loop,
   and watch `k get hpa -w`. Time how long scale-down takes after you stop the load. Why?

## Session 2: scheduling (W14 D2)

1. Taint the "GPU" node: `k taint nodes -l pool=gpu gpu=true:NoSchedule`. Scale `web` to 12: none land there.
2. Run a pod with the toleration only, then with toleration + `nodeSelector: {pool: gpu}`. Where does each land?
3. Unschedulable: a pod requesting `cpu: 64`. `k describe pod`: read the `FailedScheduling` message; it lists
   why each node was rejected (the filter phase, in words).
4. Fake GPUs. Advertise an extended resource on the GPU node
   (https://kubernetes.io/docs/tasks/administer-cluster/extended-resource-node/):
   ```bash
   NODE=$(k get nodes -l pool=gpu -o name | cut -d/ -f2)
   k proxy &
   curl --header "Content-Type: application/json-patch+json" --request PATCH \
     --data '[{"op": "add", "path": "/status/capacity/example.com~1gpu", "value": "8"}]' \
     http://localhost:8001/api/v1/nodes/$NODE/status
   k describe node $NODE | grep -A8 Capacity
   ```
   Now pods can request `resources.limits: {example.com/gpu: 4}`. Start three of them: the third stays
   Pending. The scheduler counts requests, exactly as in the lab.

## Session 3: queues and gangs with Kueue (W14 D4)

1. Install Kueue from its releases page (pick the current version):
   `k apply --server-side -f https://github.com/kubernetes-sigs/kueue/releases/download/<version>/manifests.yaml`
2. Create one `ResourceFlavor`, two `ClusterQueue`s in one cohort with a nominal quota of 4
   `example.com/gpu` each, and a `LocalQueue` per namespace (`team-x`, `team-y`). Start from the "single
   cluster queue setup" example in the Kueue docs and add the cohort and the extended resource; the API
   group/version in the examples matches the version you installed.
3. Submit a `Job` from team-y with `parallelism: 3`, each pod asking 2 fake GPUs (6 > its quota of 4), label
   `kueue.x-k8s.io/queue-name`. It is admitted by borrowing. `k get workloads -A`.
4. Submit a 4-GPU job from team-x. Enable `reclaimWithinCohort: Any` in team-x's ClusterQueue preemption
   settings first. Predict, then watch team-y's job get suspended and its pods deleted.
5. Gang behaviour: submit a job needing 16 GPUs. It stays suspended and holds nothing (compare with step 4
   of session 2 where plain pods were bound one by one).

## Session 4 (optional): an inference gateway without GPUs

Install the Gateway API CRDs, a gateway implementation, and the Gateway API Inference Extension with
the **llm-d inference simulator** as fake model servers (it speaks the OpenAI API and exports vLLM-style
metrics): https://gateway-api-inference-extension.sigs.k8s.io/ (getting started) ·
https://github.com/llm-d/llm-d-inference-sim
Goal: send requests through the gateway, read the `InferencePool`, find the queue-depth metric the
endpoint picker uses, and scale the simulator with KEDA on that metric instead of CPU.

Clean up: `kind delete cluster --name staff`.
