# W9 D1: collectives by hand: ring all-reduce

Primer: `knowledge/09-distributed-training.md` §1.

## The one idea

Data-parallel training ends every step with an **all-reduce**: every worker needs the sum (then
mean) of all workers' gradients. The **ring** algorithm (Baidu 2017, NCCL's default for large
messages) is bandwidth-optimal:

1. Split each worker's buffer into **N chunks**.
2. **Reduce-scatter, N−1 steps:** at step s, worker i sends chunk `(i − s) mod N` to worker i+1, which
   adds it to its own copy. After N−1 steps, worker i holds the **full sum of chunk `(i + 1) mod N`**.
3. **All-gather, N−1 steps:** at step s, worker i sends its completed chunk `(i + 1 − s) mod N` to i+1,
   which overwrites. After N−1 steps everyone has every summed chunk.

Each worker sends `2·(N−1)/N · size` bytes in total: **almost independent of N**. A parameter server
receives `(N−1)·size` at the server: it does not scale.

Today the "workers" are numpy arrays in one process, and the "network" is a function call that
counts elements sent. The algorithm is exactly the real one.

## Today's build (`w9d1_collectives.py`)

`chunk_bounds(L, N)`, `reduce_scatter(bufs)` (in place, returns elements sent per worker),
`all_gather(bufs)`, `ring_allreduce(bufs) -> (results, elements_sent_per_worker)`,
`ring_bytes_per_worker(N, size_bytes)`, `param_server_bytes_at_server(N, size_bytes)`.

## Staff angle

At scale, communication is the budget. A 7B model in bf16 has 14 GB of gradients per step;
on 8 GPUs with NVLink (~450 GB/s effective per GPU) ring all-reduce costs ~55 ms; across nodes on 400 Gb/s
InfiniBand (~50 GB/s) it costs ~500 ms unless overlapped with backward (DDP buckets) or reduced
(ZeRO/FSDP reduce-scatter, gradient compression). A staff engineer can say where the time goes before
reading a profiler.
