# Week 9: Distributed training infrastructure

**Everything you need for this week is on this page.** You need week 8 (the PyTorch training loop) and week 3 (replication vocabulary). Everything runs on CPU, with two local processes for the distributed lab. Nothing from other folders is required.

"What breaks when you go from 1 GPU to 64?" is the question that separates people who have run large training jobs from people who have read about them. This week you build the parts yourself, at toy size and with exact tests: the communication step at the heart of every multi-GPU job, a two-process run that must equal the single-process one, a resume that is exact to the bit, the memory arithmetic that decides what fits, and checkpoints that survive a node dying halfway through a save.

## Start here

1. Read [The week in one table](#the-week-in-one-table) and [Distributed training in ten minutes](#distributed-training-in-ten-minutes).
2. Each day, open that day's folder and follow [What to do each day](#what-to-do-each-day).
3. The lesson for each day is the matching section of this page: [Day 1](#day-1-ring-all-reduce), [Day 2](#day-2-ddp-on-two-processes), [Day 3](#day-3-bit-exact-resume), [Day 4](#day-4-memory-arithmetic-and-zero), [Day 5](#day-5-sharded-checkpoints-efficiency-then-a-design).
4. Friday: [End of the week](#end-of-the-week).

### What is in a day folder

| File | What it is | You |
|---|---|---|
| `predict.md` | small questions, answered before you read anything | write guesses |
| `README.md` | one-page summary of the day, with its "staff angle" | read after the lesson |
| `predict_run.py` | prints the real answers | run, compare |
| `w9dN_*.py` | **the exercise**, with `# TODO` | **write the code** |
| `test_w9dN_*.py` | tests | run, never edit |
| `review_w9dN.py` + its test | code with one planted bug | **find and fix**, write the `WHY:` line |
| `questions.md` | interview questions | answer out loud |

Friday's folder also has `design.md` (the prompt) and `rubric.md`. You write your answer in a new file, `my_design.md`.

### What to do each day

One hour, commands from the repo root.

| Min | Step | Command or file |
|---|---|---|
| 0–5 | Retrieve (Monday: 10-min delayed recall of last week's hardest function instead) | `uv run python scripts/review.py` |
| 5–10 | Guess, before reading | `predict.md` |
| 10–18 | Read the lesson | the day's section on this page |
| 18–20 | Check your guesses | `uv run python weeks/w9-distributed-training/<day>/predict_run.py` |
| 20–45 | Build, narrating out loud | `uv run pytest weeks/w9-distributed-training/<day> -k "not review"` until green |
| 45–53 | Review | `uv run pytest weeks/w9-distributed-training/<day> -k review` |
| 53–60 | Explain | `questions.md` out loud, then `uv run python scripts/review.py add weeks/w9-distributed-training/<day>` |

Guess before reading even if you know nothing: a wrong guess makes the lesson stick (`LEARNING.md` rule 1). AI stays off in the exercise files; stuck for 10 minutes, ask for a hint, not code.

## The week in one table

| Day | Folder | The question | You build | The review bug is about |
|---|---|---|---|---|
| Mon | `d1-collectives` | how do N workers share their gradients? | ring all-reduce, by hand | a chunk index |
| Tue | `d2-ddp-gloo` | is my distributed run the same as one process? | data-parallel training on two real processes | a missing division |
| Wed | `d3-exact-resume` | can I stop and continue as if nothing happened? | a checkpoint that restores everything | one piece of state |
| Thu | `d4-memory-zero` | what fits on a GPU? | memory arithmetic; a ZeRO-1 optimiser step | which shard a rank updates |
| Fri | `d5-sharded-checkpoints` | what if a node dies during a save? | sharded checkpoints with a manifest; resharding; efficiency metrics; then a timed design | the order of two writes |

## Distributed training in ten minutes

**Training, in one paragraph.** A model has parameters. For a batch of examples you compute a loss, then its **gradient**: for each parameter, the direction that lowers the loss. The **optimiser** moves each parameter a small step in that direction. Repeat millions of times.

**Why several GPUs.** One GPU is too slow for a large model, and often too small to hold it. The standard answer is **data parallelism**: every GPU holds a full copy of the model, each processes a different slice of the batch, and before the update they combine their gradients so that all copies take the **same** step and stay identical.

| Word | Meaning |
|---|---|
| worker, rank | one process (usually one GPU). Ranks are numbered 0 to N−1; rank 0 does the logging and saving |
| world size | the number of ranks, `N` or `W` |
| collective | a communication operation in which all ranks take part |
| all-reduce | the collective that gives every rank the sum (or mean) of a value over all ranks |
| DDP | distributed data parallel: PyTorch's name for the scheme above |
| checkpoint | everything saved to disk so that training can continue later |
| preemption | the cluster takes your machines back with little warning; it happens daily on shared clusters |
| Adam | the usual optimiser. It keeps two running averages per parameter (`m` and `v`), so its state is twice the size of the model |
| mixed precision | computing in 16-bit numbers for speed while keeping a 32-bit master copy of the parameters for accuracy |

The theme of the week is one sentence: **a distributed run is correct only if it gives the same result as the simple run it replaces.** Each day's test is an exact comparison of that kind. It is the test to demand of any training code you review.

## Day 1: Ring all-reduce

Folder: `d1-collectives`. Exercise: `w9d1_collectives.py`.

### The operation

At the end of every step each of the `N` workers has its own gradient, a long array. Every worker needs the **sum** over all workers. That is an all-reduce.

### The naive way and why it fails

Send everything to one machine (a **parameter server**), add, send the result back. That machine receives `(N − 1) × size` bytes per step. With 64 workers and a 10 GB gradient, 630 GB arrive at one network card, every step. It does not scale.

### The ring

Arrange the workers in a ring: each sends only to its right-hand neighbour. Cut each worker's array into **N chunks**. Two phases of `N − 1` steps each.

**Phase 1, reduce-scatter.** At step `s`, worker `i` sends its chunk number `(i − s) mod N` to worker `i + 1`, which **adds** it to its own copy of that chunk. Partial sums travel around the ring and grow. After `N − 1` steps, worker `i` holds the **complete sum** of chunk `(i + 1) mod N`.

**Phase 2, all-gather.** Each worker now owns one finished chunk. At step `s`, worker `i` sends chunk `(i + 1 − s) mod N` to worker `i + 1`, which **overwrites** its copy. After `N − 1` steps everyone holds every finished chunk.

A trace with `N = 3`, looking only at chunk 0 (values `a0, b0, c0` on workers 0, 1, 2):

```
reduce-scatter
  step 0: worker 0 sends chunk 0 → worker 1 now has a0 + b0
  step 1: worker 1 sends chunk 0 → worker 2 now has a0 + b0 + c0       complete on worker 2
all-gather
  step 0: worker 2 sends chunk 0 → worker 0 overwrites
  step 1: worker 0 sends chunk 0 → worker 1 overwrites                  everyone has the sum
```

Worker 2 ends with chunk 0 complete, and `(2 + 1) mod 3 = 0`: the rule holds.

**All sends of one step happen at the same time.** In a simulation, a loop over workers would let worker 1 receive and then send a value it should not have yet. Take a snapshot of what each worker sends **before** applying any addition of that step.

### The cost

Each worker sends `(N − 1)` chunks of size `size / N` in each phase:

```
bytes sent per worker = 2 · (N − 1) / N · size          just under 2 × size, whatever N is
```

Almost independent of `N`. That is why it scales, and why NCCL, the library under PyTorch on NVIDIA GPUs, uses it for large messages.

### Cutting into chunks

`L` elements into `N` contiguous chunks: each gets `L // N`, and the first `L % N` chunks get one more. Ten elements in three chunks: sizes 4, 3, 3.

### Traps of the day

- A chunk index off by one in either phase.
- Sends applied one worker at a time within a step.
- Adding in the all-gather phase, or overwriting in the reduce-scatter phase.
- Chunks that do not cover all the elements when `L` is not a multiple of `N`.

### Today's build

| Function | Job | Lesson section |
|---|---|---|
| `chunk_bounds` | `N` contiguous chunks covering `L` elements | cutting into chunks |
| `reduce_scatter` | phase 1, in place; elements sent per worker | the ring |
| `all_gather` | phase 2, in place | the ring |
| `ring_allreduce` | both phases on copies; results and elements sent | the ring |
| `ring_bytes_per_worker`, `param_server_bytes_at_server` | the two costs | the cost; the naive way |

Run: `uv run pytest weeks/w9-distributed-training/d1-collectives -k "not review"`

---

## Day 2: DDP on two processes

Folder: `d2-ddp-gloo`. Exercise: `w9d2_ddp.py`.

### The correctness condition

Data-parallel training must compute **the same update as one process on the whole batch**. Suppose the loss is a mean over the examples. One process on a batch of 8 computes the mean gradient over 8. Two ranks with 4 examples each compute two local means. Then:

```
gradient of the global mean = (1 / W) · Σ over ranks of (local mean gradient)        when all ranks have the same batch size
```

So the ranks all-reduce their gradients with a **sum**, then **divide by the world size**. Without the division every step is `W` times too large: the learning rate has been multiplied by `W` in silence. On 2 ranks the run still trains, a little unstable. On 64 it diverges and people blame the model. That is today's review bug.

### The test

Run two real processes that talk through `torch.distributed`, each on half of every global batch, and compare the final weights with one process on the full batch. They must match to floating-point tolerance. Not "a similar loss curve": the same numbers.

### What a worker does

```
torch.distributed.init_process_group("gloo", init_method=..., rank=rank, world_size=world)     # gloo: the CPU backend
for each step:
    take THIS rank's slice of the global batch
    loss = mean over the local slice;  loss.backward()
    for each parameter:  all_reduce(p.grad, SUM);  p.grad /= world
    optimiser step
rank 0 saves the result
torch.distributed.destroy_process_group()
```

`torch.distributed.all_reduce(tensor, op=torch.distributed.ReduceOp.SUM)` replaces the tensor, in place and on every rank, by the sum over all ranks. Every rank must call the collectives in the same order, or the group waits forever.

Both models must **start identical**: same seed for the initial weights on every rank.

### Sharding the data

Each rank must see a different part of the data, and together they must see all of it. The usual scheme (PyTorch's `DistributedSampler`): every rank builds the **same** seeded shuffle of all the indices, pads it so its length is a multiple of the world size, and rank `r` takes every `W`-th index starting at `r`.

```python
perm = list(range(10)); world = 4
perm = perm + perm[: (-len(perm)) % world]        # pad to 12 by repeating from the start
[perm[r::world] for r in range(world)]            # four disjoint-by-position slices of equal length
```

The seed includes the **epoch**, so each epoch has a new order. With a constant seed every epoch replays the same order.

### Traps of the day

- No division by the world size.
- A different seed on each rank for the shuffle: the slices overlap and miss data.
- A different initial model on each rank.
- Rank 1 also saving: two processes writing one file.

### Today's build

| Function | Job | Lesson section |
|---|---|---|
| `shard_indices` | this rank's indices for an epoch | sharding the data |
| `average_gradients` | all-reduce each gradient, divide by the world size | the correctness condition |
| `train_single` | the reference: one process, full batch | the test |
| `ddp_worker` | one rank of the distributed run | what a worker does |

`run_ddp` (provided) starts the processes. This lab takes longer than the others to run.

Run: `uv run pytest weeks/w9-distributed-training/d2-ddp-gloo -k "not review"`

---

## Day 3: Bit-exact resume

Folder: `d3-exact-resume`. Exercise: `w9d3_resume.py`.

### Why exact

A long run will be interrupted: preemption, a dead node, a deploy. If resuming gives a run that is only "about the same", you can never again compare two runs: any difference might come from the interruptions. Resume must reproduce **exactly** the run you would have had.

### Everything that influences the future

| State | Forget it and… |
|---|---|
| model parameters | you restart from scratch |
| **optimiser state** (Adam's `m`, `v`, step count) | the first steps after resume behave like a fresh Adam: the loss jumps |
| learning-rate scheduler state | warm-up starts again, or the learning rate jumps |
| step and epoch counters | schedules and data order shift |
| **random generator states**: torch, numpy, Python's `random` | different dropout and different data: the run drifts away with no error |
| position in the data | examples repeated or skipped |

The random generators are the ones people forget. There are three separate ones and all three must be saved:

```python
import random, numpy as np, torch
state = (torch.get_rng_state(), np.random.get_state(), random.getstate())
a = (torch.rand(1).item(), np.random.rand(), random.random())
torch.set_rng_state(state[0]); np.random.set_state(state[1]); random.setstate(state[2])
a == (torch.rand(1).item(), np.random.rand(), random.random())        # True: the same draws again
```

Models, optimisers and schedulers each have `.state_dict()` to save and `.load_state_dict(...)` to restore.

**Order when loading.** Rebuilding the model consumes random numbers (for the initial weights). So restore the random states **last**, after everything has been rebuilt. Restored first, they are immediately disturbed by the rebuild.

### Atomic save

A crash in the middle of writing a checkpoint must not destroy the previous one. Write to a temporary file, then rename it over the real name. A rename is **atomic**: at every instant the real name points either to the complete old file or to the complete new one.

```python
import os, tempfile
d = tempfile.mkdtemp(); path = os.path.join(d, "ckpt.pt")
torch.save({"step": 10}, path + ".tmp")
os.replace(path + ".tmp", path)                    # atomic
torch.load(path, weights_only=False)               # {'step': 10}
```

`weights_only=False` is needed because the checkpoint holds numpy and Python objects, not only tensors. Use it only on files you wrote yourself.

### The test

Train 20 steps in one go. Separately: train 10, save, throw everything away, rebuild, load, train 10 more. The final parameters must be **identical**. If they are merely close, one piece of state is missing; the table tells you where to look.

### Traps of the day

- No optimiser state.
- One of the three random generators forgotten.
- Random states restored before the rebuild.
- A save that writes directly to the final path.

### Today's build

| Function | Job | Lesson section |
|---|---|---|
| `save_checkpoint` | everything in the table, atomically | everything that influences the future; atomic save |
| `load_checkpoint` | rebuild, then restore, random states last | order when loading |

`build` and `train_steps` are provided; `train_steps` uses all three random generators on purpose.

Run: `uv run pytest weeks/w9-distributed-training/d3-exact-resume -k "not review"`

---

## Day 4: Memory arithmetic and ZeRO

Folder: `d4-memory-zero`. Exercise: `w9d4_zero.py`.

### 16 bytes per parameter

Mixed-precision training with Adam keeps, for each parameter:

| What | Bytes |
|---|---|
| 16-bit parameters, used for computing | 2 |
| 16-bit gradients | 2 |
| 32-bit master parameters | 4 |
| Adam's first average `m`, 32-bit | 4 |
| Adam's second average `v`, 32-bit | 4 |
| **total** | **16** |

So a model with `Ψ` parameters needs `16 Ψ` bytes of **model states**, before any activation. A 7-billion-parameter model: 112 GB. It does not fit on an 80 GB GPU, and plain data parallelism does not help, since every GPU holds a full copy.

### ZeRO: stop replicating

**ZeRO** observes that with `N` ranks there are `N` identical copies of everything, and shares the states out instead. Each rank **owns** one slice (a **shard**) of the parameter vector.

| Mode | What is sharded | Bytes per GPU |
|---|---|---|
| DDP | nothing | `16 Ψ` |
| ZeRO-1 | optimiser states (master, `m`, `v`: 12 of the 16) | `2Ψ + 2Ψ + 12Ψ / N` |
| ZeRO-2 | + gradients | `2Ψ + 14Ψ / N` |
| ZeRO-3 (FSDP in PyTorch) | + parameters | `16Ψ / N` |

With 8 ranks, ZeRO-1 takes that 7B model from 112 GB to `28 + 10.5 = 38.5` GB per GPU. Each further stage saves more memory and costs more communication.

### Adam, by hand

```
m ← β1 · m + (1 − β1) · g                 running average of the gradient
v ← β2 · v + (1 − β2) · g²                running average of its square
m̂ = m / (1 − β1^t)     v̂ = v / (1 − β2^t)      bias correction; t counts steps from 1
p ← p − lr · m̂ / ( sqrt(v̂) + ε )
```

`m` and `v` start at zero, so their first values are too small. The correction divides them back up; it matters only during the first steps. With `t` starting at 0 the correction divides by zero.

### ZeRO-1 in one sentence

Every rank computes the full averaged gradient, but **updates only its own shard** of the parameters, using only **its own shard** of `m` and `v`; then the updated shards are gathered so that every rank has the full new parameter vector.

The result must be **identical to ordinary Adam** on the full vector: each parameter is updated exactly once, by its owner, with the same numbers. That is today's test, and the week's theme again. A rank that updates the wrong slice, or the whole vector, breaks it. That is today's review bug.

### Traps of the day

- `t` starting at 0.
- A rank using its shard of `m`, `v` with the wrong slice of the gradient.
- Gradients not averaged before the update.
- GB and GiB mixed up in the arithmetic: the docstring fixes the unit.

### Today's build

| Function | Job | Lesson section |
|---|---|---|
| `model_state_bytes` | bytes per GPU for each mode | 16 bytes per parameter; ZeRO |
| `max_params` | the largest model that fits | ZeRO |
| `adam_step` | one Adam step with numpy | Adam, by hand |
| `zero1_step` | average, update own shard, gather | ZeRO-1 in one sentence |

Run: `uv run pytest weeks/w9-distributed-training/d4-memory-zero -k "not review"`

---

## Day 5: Sharded checkpoints, efficiency; then a design

Folder: `d5-sharded-checkpoints`. Exercise: `w9d5_ckpt.py`. Also in the folder: `design.md`, `rubric.md`.

### Checkpoints at scale

With sharded states (yesterday), no single process holds the whole model, so each rank writes its **own shard** to disk. A checkpoint is complete only when **all** shards are written. Nodes die during saves. The pattern that stays correct:

1. Each rank writes `step-XXXX/shard-r-of-N.pt`, atomically (temporary file, then rename: Wednesday).
2. When every rank has finished, rank 0 writes `step-XXXX/manifest.json` **last**. The manifest lists the world size, the step, and a **checksum** of every shard.
3. A loader trusts a step **only if** its manifest exists **and** every shard it lists exists with a matching checksum.

The manifest is the "commit" of the checkpoint. A save interrupted halfway leaves a directory with no manifest: the loader ignores it and falls back to the previous complete step.

Write the manifest **first** and the meaning is lost: a manifest can then exist while shards are missing. That is today's review bug. The checksum check is the second line of defence: it also catches a shard damaged on disk.

```python
import hashlib
hashlib.sha256(b"the bytes of a shard file").hexdigest()[:16]      # change one byte, the checksum changes
```

`latest_complete` looks at every step directory and returns the highest step that passes the test. Sort steps as numbers.

### Resharding

Restart the job with a different number of GPUs (an **elastic** restart): the old shards do not fit the new world size. Concatenate the old shards in rank order into one flat vector, then cut it again for the new world size, with Monday's rule for uneven sizes.

### Two efficiency numbers

**MFU, model FLOPs utilisation**: of the arithmetic the GPUs could do at their peak, what fraction went into the model?

```
MFU = 6 · parameters · tokens per second / ( number of GPUs · peak FLOPs per GPU )
```

The 6: about 2 floating-point operations per parameter and per token for the forward pass and 4 for the backward pass. 40 to 55% is good for a large model. A low MFU means the GPUs wait: for data, for communication, for the slowest rank.

**Goodput**: the fraction of wall-clock time spent on training that was **kept**. Time lost to restarts, to steps redone after a failure and to waiting in a queue is not useful. A cluster can show GPUs busy 95% of the time and have a goodput of 60%.

### After the lab: the Friday design (45 minutes, timed)

`design.md`: a multi-node training platform.

1. Start a 45-minute timer. Write in `my_design.md`, following the 45-minute frame of [week 5](../w5-design-method/README.md#the-45-minute-frame). Stop at the bell.
2. Grade yourself with `rubric.md`.
3. Only then read the model answer: `model_answer.md`, in the same folder on the `solutions` branch.
4. Write in `PROGRESS.md` the one thing that would have raised your level.

This week's deep dives: all-reduce cost, the exactness test, resume, the memory table, checkpoint commit, MFU and goodput.

### Traps of the day

- The manifest written before the shards.
- A step trusted because its directory exists.
- Shards concatenated in file-name order as text (`shard-10` before `shard-2`).
- Steps sorted as text.

### Today's build

| Function | Job | Lesson section |
|---|---|---|
| `save_shard` | one rank's shard, atomically | checkpoints at scale |
| `write_manifest` | step, world size, checksum per shard, written last | checkpoints at scale |
| `is_complete`, `latest_complete` | the trust test; the newest complete step | checkpoints at scale |
| `load_full`, `reshard` | concatenate; cut for a new world size | resharding |
| `mfu`, `goodput` | the two efficiency numbers | two efficiency numbers |

Run: `uv run pytest weeks/w9-distributed-training/d5-sharded-checkpoints -k "not review"`

---

## End of the week

- **AI-off gate (15 min):** one drill from `drills/w09`, timer on, AI fully off: `uv run pytest drills/w09 -k d<number>`. Protocol: `drills/README.md`.
- **Reading slot (20 min, read only):** this week's file is row 9 of `reading/README.md`.
- **Ship one public thing** and log it in `SHIPLOG.md`: one claim, one piece of evidence. A write-up of this week's hardest lab with its numbers counts.
- **Tick `PROGRESS.md`**, write the retro, and name the hardest lab: next Monday you rewrite its main function from a blank file.

You are done with week 9 when you can do these without notes:

- [ ] explain ring all-reduce in two phases and why its cost does not grow with `N`
- [ ] state the correctness condition of data parallelism and the bug of the missing division
- [ ] list everything a checkpoint must hold for an exact resume, and the order of restoring
- [ ] derive 16 bytes per parameter and the per-GPU memory of ZeRO-1, 2 and 3
- [ ] write an Adam step
- [ ] explain why the manifest is written last
- [ ] define MFU and goodput
- [ ] answer "what breaks from 1 GPU to 64?": learning rate and batch size, sharding, epoch seed, who saves, stragglers, checkpoints, failures

## Optional depth (not needed for the labs)

- Interview questions with short answers: `knowledge/09-distributed-training.md`
- Previous week: [`../w8-reward-models/README.md`](../w8-reward-models/README.md) · Next: [`../w10-harness-serving/README.md`](../w10-harness-serving/README.md)
