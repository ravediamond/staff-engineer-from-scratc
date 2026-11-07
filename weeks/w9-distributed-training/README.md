# Week 9: distributed training infrastructure

You do not need a GPU cluster to understand one. Everything that goes wrong at 512 GPUs has
a 2-process CPU version: collectives that move the wrong bytes, gradients summed instead of
averaged, resumes that are "almost" identical, memory budgets off by 4×, checkpoints that are
half-written when the node dies. This week builds each one with `gloo` on your Mac, then a
Friday design of the platform.

Primer: `knowledge/09-distributed-training.md`.

| Day | Lab | Review bug |
|---|---|---|
| d1 | ring all-reduce by hand: reduce-scatter + all-gather, byte counting | chunk index off by one in reduce-scatter |
| d2 | DDP on 2 `gloo` processes == single process on the global batch | gradients summed, not averaged |
| d3 | bit-exact resume: model, optimizer, scheduler, every RNG | optimizer state not checkpointed |
| d4 | memory math (DDP, ZeRO-1/2/3) and ZeRO-1 optimizer sharding | Adam counted as one state |
| d5 | sharded checkpoints, manifests, resharding, MFU + **Friday design** | trusts a manifest whose shards are missing |
