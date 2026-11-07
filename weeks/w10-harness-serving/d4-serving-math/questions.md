# Questions

1. Derive KV-cache size per token. How does GQA change it?
2. Why is decoding memory-bandwidth-bound, and what does that imply for batching?
3. Static vs continuous batching: explain and quantify the difference on a mixed workload.
4. What does PagedAttention fix, and what else does paging enable?
5. Your p99 latency is bad at high load but GPU utilisation looks fine. Hypotheses?

## Model answers

1. Per layer, per token: one K and one V vector per KV head: 2 × kv_heads × head_dim values; times layers and bytes per value. GQA shares KV heads across query heads (e.g. 32 query heads, 8 KV heads), cutting KV size 4× with small quality loss; MQA uses 1 KV head.
2. Each decode step reads all weights (and the KV cache) from HBM to produce one token per sequence. Arithmetic intensity is low at batch 1, so time ≈ bytes read / bandwidth. Batching amortizes the weight reads over many sequences: throughput rises almost linearly with batch until compute-bound or KV memory runs out.
3. Static: the batch occupies all slots until the longest sequence finishes, so short requests wait (head-of-line blocking) and slots sit idle. Continuous: finished slots refill every step. On mixed lengths, throughput improves 2–20× and latency for short requests drops sharply (in today's simulation, more than 2× lower mean latency).
4. Fragmentation from pre-allocating max length (60–80% waste in naive systems) drops to under one block per sequence, so 2–4× more concurrent sequences fit. Paging also enables prefix sharing (copy-on-write blocks for shared system prompts, parallel sampling, beam search) and prefix caching across requests.
5. Queueing (arrival rate near capacity, so latency explodes nonlinearly), prefill of long prompts stalling decode steps (fix with chunked prefill or prefill/decode disaggregation), KV memory pressure causing preemption and recomputation, uneven load across replicas (routing), or long outputs hogging slots. Utilization can be high while users wait.
