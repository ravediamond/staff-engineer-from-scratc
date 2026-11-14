# Questions

1. Derive the KV-cache size per token and the maximum concurrency of a model on a GPU. What caps batch size in practice?
2. Why is GPU utilisation a bad autoscaling signal for LLM servers? Name three good ones and how they reach the HPA.
3. Break down the cold start of a 70B replica and give four ways to shorten it. When is scale-to-zero acceptable?
4. Why not put a plain Service (round-robin) in front of vLLM pods? What does an inference-aware gateway look at?
5. You must serve 200 fine-tuned LoRA adapters of one base model. Design the serving layer.
6. Which pieces would you name for: single-node serving, multi-node serving of one huge model, distributed fine-tuning, quotas? (One Kubernetes-native project each.)

