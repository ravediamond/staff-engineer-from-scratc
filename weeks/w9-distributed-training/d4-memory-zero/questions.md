# Questions

1. Derive 16 bytes per parameter for mixed-precision Adam.
2. ZeRO-1, 2, 3: what is sharded, and what is the communication cost of each vs DDP?
3. What dominates memory besides model states, and how do you reduce it?
4. FSDP vs tensor parallelism vs pipeline parallelism: when each? How do they combine (3D parallelism)?
5. Plan memory for fine-tuning a 70B model with LoRA on 8 × 80 GB GPUs.

