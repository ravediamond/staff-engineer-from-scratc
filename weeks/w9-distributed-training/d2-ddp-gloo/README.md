# W9 D2: DDP on two gloo processes

Primer: `knowledge/09-distributed-training.md` §2.

## The one idea

Data parallelism is correct only if it computes **the same update as one process on the global
batch**. With a loss averaged over each rank's local batch:

```
global mean gradient = (1/W) · Σ_ranks (local mean gradient)      when every rank has the same local batch size
```

So: `all_reduce(grad, SUM)` then **divide by world size**. Forget the division and you have silently
multiplied the learning rate by W.

The test of correctness is exact: run 2 processes with `torch.distributed` (`gloo` backend, CPU),
each on half of every global batch, and compare final weights with a single process on the full batch.
They must match to floating-point tolerance. This is the test you should demand of any distributed
training code you review.

Data sharding: `shard_indices` mimics `DistributedSampler`: same seeded permutation on every rank,
padded to a multiple of world size, rank r takes `r::world`.

## Today's build (`w9d2_ddp.py`)

`shard_indices(n, world, rank, seed, epoch)`, `make_data(seed)` (provided), `average_gradients(model, world)`,
`train_single(steps, global_batch, lr)`, `ddp_worker(rank, world, init_file, out_file, steps, global_batch, lr)`,
`run_ddp(world, steps, global_batch, lr, tmpdir)` (spawns the processes and returns rank 0's weights).

## Staff angle

At 512 GPUs nobody can eyeball correctness. The staff practice is an **equivalence test suite** that
runs in CI on CPU: N-process == 1-process for a few steps, resume == no-resume (D3), sharded checkpoint
round-trip == original (D5). These catch the silent bugs (wrong reduction, double scaling with gradient
accumulation, unsynchronised dropout seeds, wrong sampler seeding) that otherwise surface as "the loss
curve looks a bit worse at scale".
