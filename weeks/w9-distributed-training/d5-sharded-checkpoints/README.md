# W9 D5: sharded checkpoints, manifests, resharding, MFU + Friday design

Primer: `knowledge/09-distributed-training.md` §5.

## The one idea

At scale every rank writes its own shard (no single process can hold the full state). A checkpoint
is complete only when **all** shards are written. The pattern:

1. each rank writes `step-XXXX/shard-r-of-N.pt` atomically (tmp + rename);
2. after a barrier, rank 0 writes `step-XXXX/manifest.json` **last**: world size, step, and a checksum per shard;
3. a loader trusts a step **only if** the manifest exists **and** every listed shard exists with the right checksum.

A node dying mid-save leaves a step directory without a manifest, or (if someone wrote the manifest
first) a manifest pointing at missing shards: the loader must skip it and fall back to the previous step.

**Resharding** (elastic restart with a different world size): concatenate the old shards in order, split
for the new world size. Today: flat 1-D parameter shards, as in ZeRO-3/FSDP's flat parameters.

**MFU** (model FLOPs utilisation), the headline efficiency number of training infra:
`MFU = 6 · params · tokens_per_second / (n_gpus · peak_flops_per_gpu)` (6 = forward 2 + backward 4
FLOPs per parameter per token, ignoring attention). 40–55% is good for large dense models.

## Today's build (`w9d5_ckpt.py`)

`save_shard(dir, step, rank, world, tensor)`, `write_manifest(dir, step, world)`, `latest_complete(dir)`,
`load_full(dir, step)`, `reshard(full, new_world)`, `mfu(params, tokens_per_s, n_gpus, peak_flops)`,
`goodput(useful_seconds, wall_seconds)`.

## Friday design (45 min)

`design.md`: a multi-node training platform. Timer, `my_design.md`, `rubric.md`, model answer on `solutions`.

## Staff angle

Training platforms are judged on **goodput**: the fraction of paid GPU-hours that produce useful
training progress. Failures, restarts from stale checkpoints, slow checkpoints, stragglers and queueing
all eat it. A staff design starts from a goodput budget ("at 2,000 GPUs, a failure every ~3 hours; with
10-minute recovery and 30-minute checkpoint intervals we lose ~X%") and works backwards to checkpoint
frequency, async saving, hot spares and fast restart.
