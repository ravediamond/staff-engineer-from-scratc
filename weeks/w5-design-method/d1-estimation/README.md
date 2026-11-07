# W5 D1: back-of-the-envelope estimation

Primer: `knowledge/05-design-method-and-estimation.md` §2 (numbers every engineer should know).

## The one idea

Estimation is not about precision. It is about **order of magnitude, fast, with stated
assumptions**, so the design matches the load. Five conversions cover 90% of interviews:

| From | To | Rule |
|---|---|---|
| DAU × actions/day | average QPS | ÷ 86,400 (≈ 10⁵ s/day) |
| average QPS | peak QPS | × 2–10 (say your factor) |
| items/day × bytes × days × replication | storage | 1 KB × 1M/day ≈ 1 GB/day ≈ 365 GB/yr |
| QPS × bytes | bandwidth | **× 8 for bits/s** (network gear speaks bits) |
| GPU-seconds of work per second | GPUs | ceil, then add headroom |

**LLM serving** adds two numbers per GPU (measured, never guessed in production): prefill
throughput (input tokens/s, compute-bound, fast) and decode throughput (output tokens/s
aggregate across the batch, memory-bandwidth-bound, slower). GPUs needed ≈
`peak_qps · (in_tokens / prefill_rate + out_tokens / decode_rate)`.

## Today's build (`w5d1_estimation.py`)

`qps(dau, actions_per_day, peak_factor) -> (avg, peak)`, `storage_bytes(...)`, `bandwidth_gbps(qps, bytes_per_request)`,
`llm_gpus(...)`, `monthly_cost(gpus, usd_per_gpu_hour, utilization)`, `human_bytes(n)`.

## Staff angle

The staff habit is to estimate **cost**, not just capacity, and to find the dominant term. "Storage
is 40 TB/yr, which is about $1k/month on object storage: irrelevant. GPU serving is $180k/month:
that is the design." Then every deep dive goes where the money or the risk is.
