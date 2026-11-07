# W10 D4: serving math: KV cache, batching, paged memory

Primer: `knowledge/11-llm-serving.md` §1–3.

## The one idea

**KV cache.** Each generated token attends to all previous tokens' keys and values, stored per layer:

```
KV bytes = 2 (K and V) × layers × kv_heads × head_dim × seq_len × batch × bytes_per_value
```
Llama-3-8B (32 layers, 8 KV heads with GQA, head_dim 128, bf16): 128 KB per token. A 32k-token context
is 4 GB **per sequence**. KV memory, not compute, usually caps concurrency.

**Batching.** Decoding one token for 1 sequence or for 64 costs almost the same time (memory-bound:
the weights are read once per step). **Static batching** waits until every sequence in the batch is done
before admitting new ones: short requests wait for long ones. **Continuous batching** (Orca, vLLM)
admits new requests at every step as slots free up: much higher throughput, lower latency.

**Paged KV (vLLM's PagedAttention).** Pre-allocating `max_len` contiguous KV per sequence wastes memory
(most sequences end early). Paged allocation uses fixed-size blocks (e.g. 16 tokens): waste is at most
one partial block per sequence.

## Today's build (`w10d4_serving.py`)

`kv_bytes_per_token(...)`, `kv_cache_bytes(...)`, `max_concurrent(gpu_gb, weights_gb, kv_per_token, tokens_per_seq)`,
`simulate(requests, max_batch, mode, step_time)` for `"static"` vs `"continuous"`, and `paged_waste` vs `contiguous_waste`.

## Staff angle

Serving cost is set by tokens/s/GPU at a latency SLO, and the levers are known: batch size (bounded by
KV memory), KV size (GQA, quantised KV cache, shorter contexts, prompt caching), and decode speed
(quantised weights, speculative decoding in D5). A staff engineer can say which lever moves the
dominant cost for a given traffic shape, before benchmarking.
