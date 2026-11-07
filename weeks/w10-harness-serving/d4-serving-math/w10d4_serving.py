"""W10 D4: KV-cache sizing, static vs continuous batching simulation, paged vs contiguous KV waste."""
import math


def kv_bytes_per_token(layers: int, kv_heads: int, head_dim: int, dtype_bytes: int = 2) -> int:
    return 2 * layers * kv_heads * head_dim * dtype_bytes


def kv_cache_bytes(layers: int, kv_heads: int, head_dim: int, seq_len: int, batch: int, dtype_bytes: int = 2) -> int:
    return kv_bytes_per_token(layers, kv_heads, head_dim, dtype_bytes) * seq_len * batch


def max_concurrent(gpu_gb: float, weights_gb: float, kv_per_token: int, tokens_per_seq: int) -> int:
    """floor((gpu - weights) bytes / (kv_per_token * tokens_per_seq)). GB = 1e9 bytes."""
    return int((gpu_gb - weights_gb) * 1e9 // (kv_per_token * tokens_per_seq))


def simulate(requests: list, max_batch: int, mode: str, step_time: float = 1.0) -> dict:
    """requests: [(arrival_step, output_tokens)] sorted by arrival. Each step, every running sequence emits one token;
    a sequence finishes at the end of the step that emits its last token.
      continuous: at the START of every step, admit waiting arrived requests (FIFO) into free slots.
      static:     admit a new batch (up to max_batch arrived requests, FIFO) only when NO sequence is running.
    If nothing is running and nothing has arrived, time advances one step (idle).
    latency of a request = finish_step - arrival_step (steps, then * step_time).
    Return {"makespan": total steps * step_time, "mean_latency": ..., "throughput": total tokens / makespan}."""
    pending = list(requests)
    running = []  # [remaining, arrival]
    t, latencies, total = 0, [], sum(o for _, o in requests)
    while pending or running:
        can_admit = mode == "continuous" or not running
        if can_admit:
            while pending and pending[0][0] <= t and len(running) < max_batch:
                a, o = pending.pop(0)
                running.append([o, a])
        t += 1
        if not running:
            continue
        still = []
        for r in running:
            r[0] -= 1
            if r[0] == 0:
                latencies.append(t - r[1])
            else:
                still.append(r)
        running = still
    makespan = t * step_time
    return {"makespan": makespan, "mean_latency": sum(latencies) / len(latencies) * step_time,
            "throughput": total / makespan}


def contiguous_waste(seq_lens: list, max_len: int) -> int:
    """Token slots reserved but unused when each sequence pre-allocates max_len."""
    return sum(max_len - s for s in seq_lens)


def paged_waste(seq_lens: list, block: int) -> int:
    """Token slots unused in the last partial block of each sequence."""
    return sum(math.ceil(s / block) * block - s for s in seq_lens)
