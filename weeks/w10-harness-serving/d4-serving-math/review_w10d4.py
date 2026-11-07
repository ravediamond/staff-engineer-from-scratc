"""Review: GPU sizing sheet for the inference fleet. Production OOMs at half the concurrency it promised.
Find the bug, fix it, explain:

WHY:
"""


def kv_gb(layers, kv_heads, head_dim, seq_len, batch, dtype_bytes=2):
    return 2 * layers * kv_heads * head_dim * seq_len * batch * dtype_bytes / 1e9
