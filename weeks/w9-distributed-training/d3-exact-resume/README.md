# W9 D3: bit-exact resume

Primer: `knowledge/09-distributed-training.md` §3.

## The one idea

A long training run will be interrupted (preemption, node failure, deploy). Resuming must produce
**exactly** the run you would have had without the interruption, or you can never trust a
comparison between runs again. That requires saving **all** state that influences the future:

| State | Forget it and… |
|---|---|
| model parameters | obvious |
| **optimizer state** (Adam's m, v, step count) | the first steps after resume behave like a fresh Adam: loss spike |
| LR scheduler state | warmup restarts, or the LR jumps |
| step / epoch counters | data order and schedules shift |
| **RNG states**: torch, numpy, python `random` | different dropout masks and data sampling: diverges silently |
| data loader position | samples repeated or skipped |

Save atomically: write to `path.tmp`, then `os.replace` (atomic on POSIX). A crash mid-save must leave
the previous checkpoint intact.

## Today's build (`w9d3_resume.py`)

`build(seed)` (model with dropout + Adam + LR scheduler, provided), `train_steps(state, n)` (uses torch,
numpy and python RNGs on purpose), `save_checkpoint(path, state)`, `load_checkpoint(path, seed)`,
and the equivalence test: 20 steps straight == 10 steps, save, new process-like rebuild, load, 10 steps.

## Staff angle

"Bit-exact resume" sounds pedantic until two teams argue for a week about whether a 0.3% eval
difference came from their change or from a resume. A staff engineer makes resume-equivalence a CI
test of the training stack, and makes checkpoints self-describing (config hash, code version, data
version) so any checkpoint can be traced to how it was made.
