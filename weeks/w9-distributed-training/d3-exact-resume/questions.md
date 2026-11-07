# Questions

1. List everything a checkpoint must contain for bit-exact resume.
2. Why restore RNG states last?
3. How do you make checkpoint writes crash-safe locally and on object storage?
4. What makes bit-exact resume impossible on GPUs sometimes, and what do you settle for?
5. How often should a 512-GPU job checkpoint? Derive it.

## Model answers

1. Model parameters (and buffers), optimizer state, LR scheduler state, gradient scaler state (mixed precision), step/epoch counters, RNG states (torch CPU and every CUDA device, numpy, python), data loader / sampler position, and metadata (config, code version, data version) to verify compatibility.
2. Building the model and optimizer consumes RNG (initialization); restoring RNG before that would advance it during construction and desynchronize.
3. Locally: write to a temp file, fsync, `os.replace` (atomic rename), fsync the directory. On object storage (no rename): write shards under a unique prefix, then write a small manifest last (conditional put), and readers only trust manifests (D5).
4. Non-deterministic GPU kernels (atomics in scatter-add, some cuDNN algorithms), different reduction orders under different world sizes, and asynchronous collectives. Settle for statistical equivalence (curves within noise) plus `torch.use_deterministic_algorithms(True)` in tests where possible, and bitwise equivalence on CPU tests in CI.
5. Young/Daly approximation: optimal interval ≈ √(2 × checkpoint_cost × MTBF). With 512 GPUs and a per-GPU MTBF that gives a job MTBF of ~10 hours, and a 2-minute checkpoint, the interval is √(2 × 2 min × 600 min) ≈ 49 min. Async checkpointing (snapshot to CPU memory, upload in background) lowers the cost and allows more frequent saves.
