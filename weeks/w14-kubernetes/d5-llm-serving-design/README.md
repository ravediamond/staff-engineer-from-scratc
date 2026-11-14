# W14 D5: LLM serving on Kubernetes + design #8

Primer: `knowledge/18-ml-platform-on-kubernetes.md` §4–6. Builds on W10 D4 (KV-cache sizing, continuous batching).

## The one idea

An LLM server is not a web server. Four facts change the platform design:

1. **Memory, not compute, caps concurrency.** Each running sequence holds a KV cache:
   `2 × layers × kv_heads × head_dim × bytes_per_value` per token. Concurrency =
   `(GPU memory − weights − overhead) / (context × KV per token)`.
2. **Cold start is minutes.** New node + 10 GB image + 16–140 GB of weights + load to GPU. You cannot
   autoscale your way out of a spike in seconds: keep warm replicas and headroom.
3. **GPU utilisation is a useless autoscaling signal.** With continuous batching the GPU is at ~100%
   with one request or with fifty. Scale on **queue depth**, KV-cache usage or time-to-first-token.
4. **Replicas are not interchangeable.** One has your prompt prefix cached, another has your LoRA
   adapter loaded. Round-robin throws that away; an inference-aware gateway (Gateway API Inference
   Extension: `InferencePool` + endpoint picker) routes on queue depth, cache and adapter affinity.

## Today's build (`w14d5_serving.py`)

`kv_bytes_per_token`, `max_concurrency`, `cold_start_seconds`, `cost_per_million_tokens`,
`pick_endpoint`, `desired_replicas`, and you compare two autoscaling signals in `simulate` (provided).

Then **design #8** (`design.md`): host and fine-tune LLMs on Kubernetes. 45 minutes.

## Staff angle

Derive the numbers live. "A 70B model in bf16 is 140 GB, so 4 × 80 GB GPUs with tensor parallelism,
~320 KB of KV per token, so an 8k context costs 2.5 GB per sequence" earns more than any diagram.
Then state what you would NOT build: managed endpoints for the long tail of models, self-hosting only
for the two or three that dominate the bill or cannot leave the EU.
