# 11. LLM serving

## §1 Prefill and decode

Prefill processes the prompt in parallel (compute-bound, fast per token); decode generates one token per step per
sequence (memory-bandwidth-bound). Time to first token ≈ prefill; inter-token latency ≈ decode step time.
Chunked prefill and prefill/decode disaggregation protect decode latency from long prompts.

## §2 KV cache

`2 × layers × kv_heads × head_dim × bytes` per token; GQA/MQA shrink it; quantised KV (fp8) halves it. KV memory
limits batch size and context length. Prefix (prompt) caching reuses KV for shared prefixes.

## §3 Batching and memory

Continuous batching admits new sequences every step; paged KV (blocks of ~16 tokens) removes fragmentation and
enables prefix sharing. Throughput rises with batch until compute-bound or KV-bound; latency SLOs cap the batch.

## §4 Speculative decoding

Draft k tokens, verify in one target pass, accept with `min(1, p/q)`, resample from `norm(max(0, p − q))` on rejection:
lossless. Expected tokens per pass `(1 − α^(k+1)) / (1 − α)`. Variants: Medusa/EAGLE heads, prompt lookup.

## Routing and cost levers

Prefix-aware routing (consistent hashing with bounded load) for cache hits; model routing (small model for easy
traffic, big model for hard); quantisation (weights int8/fp8/int4); autoscaling on queue depth, not CPU.

## Questions

1. Your chat product's time to first token is fine but streaming is slow. Where do you look?
<details><summary>Answer</summary>Decode step time: batch too large for the latency SLO, KV cache pressure causing preemption and recompute, long prompts' prefill interleaved with decode (use chunked prefill or disaggregation), or network/streaming buffering. Measure inter-token latency percentiles per replica and batch size.</details>

2. How do you serve 50 fine-tuned variants of the same base model cheaply?
<details><summary>Answer</summary>LoRA adapters on a shared base model with multi-LoRA serving (S-LoRA/vLLM multi-LoRA): one copy of base weights, adapters loaded on demand, requests for different adapters batched together. Hot adapters stay in GPU memory, cold ones in CPU or disk.</details>

3. Self-host vs API for an internal assistant at 2M requests/day: how do you decide?
<details><summary>Answer</summary>Compare cost per 1M tokens at your traffic shape (API price vs GPUs × utilization), quality gap between the best API model and the best open model on your evals, data and privacy constraints, latency needs, and team capacity to operate GPUs. Often: API for the hardest tasks, self-hosted small models for high-volume easy tasks, behind one gateway with routing and evals.</details>
