"""W10 D4: KV-cache sizing, static vs continuous batching simulation, paged vs contiguous KV waste."""
import math


def kv_bytes_per_token(layers: int, kv_heads: int, head_dim: int, dtype_bytes: int = 2) -> int:
    # TODO
    raise NotImplementedError


def kv_cache_bytes(layers: int, kv_heads: int, head_dim: int, seq_len: int, batch: int, dtype_bytes: int = 2) -> int:
    # TODO
    raise NotImplementedError


def max_concurrent(gpu_gb: float, weights_gb: float, kv_per_token: int, tokens_per_seq: int) -> int:
    """floor((gpu - weights) bytes / (kv_per_token * tokens_per_seq)). GB = 1e9 bytes."""
    # TODO
    raise NotImplementedError


def simulate(requests: list, max_batch: int, mode: str, step_time: float = 1.0) -> dict:
    """requests: [(arrival_step, output_tokens)] sorted by arrival. Each step, every running sequence emits one token;
    a sequence finishes at the end of the step that emits its last token.
      continuous: at the START of every step, admit waiting arrived requests (FIFO) into free slots.
      static:     admit a new batch (up to max_batch arrived requests, FIFO) only when NO sequence is running.
    If nothing is running and nothing has arrived, time advances one step (idle).
    latency of a request = finish_step - arrival_step (steps, then * step_time).
    Return {"makespan": total steps * step_time, "mean_latency": ..., "throughput": total tokens / makespan}."""
    # TODO
    raise NotImplementedError


def contiguous_waste(seq_lens: list, max_len: int) -> int:
    """Token slots reserved but unused when each sequence pre-allocates max_len."""
    # TODO
    raise NotImplementedError


def paged_waste(seq_lens: list, block: int) -> int:
    """Token slots unused in the last partial block of each sequence."""
    # TODO
    raise NotImplementedError
