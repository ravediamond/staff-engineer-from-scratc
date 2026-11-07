# Questions

1. Why must the manifest be written last, and what does the loader check?
2. How do you reshard a checkpoint for a different world size? What breaks if parameters are not flat?
3. Define MFU and goodput. Why can a job have high MFU and terrible goodput?
4. How often do large clusters fail, and how do you design for it?
5. Async checkpointing: how does it work and what are the risks?

## Model answers

1. The manifest is the commit record: it declares that all shards exist. Written first, a crash leaves a manifest pointing at missing or partial shards. The loader checks manifest presence, every listed shard's existence and checksum, and compatible metadata, and falls back to the previous complete step otherwise.
2. Gather a logical view (concatenate flat shards, or per-parameter tensors with their shard metadata), then re-split for the new world size. With per-parameter sharding along different dims (TP), you need the sharding spec per tensor (PyTorch DCP stores metadata and supports load-time resharding). The optimizer state must be resharded consistently with the parameters.
3. MFU = achieved model FLOPs / peak FLOPs while running. Goodput = useful progress / total paid time. A job can run at 50% MFU but lose half its time to failures, slow restarts, redoing work after stale checkpoints, and queueing, giving high MFU and poor goodput.
4. Hardware interruptions scale with GPU count: at ~16k GPUs, public reports show one every few hours; at 512 GPUs, roughly daily. Design: frequent async checkpoints, fast detection and automated restart, spare nodes, node health checks and quarantine, elastic resharding, and tracking lost GPU-hours as a first-class metric.
5. Snapshot state to CPU (or local NVMe) quickly, blocking only for that copy, then upload to durable storage in a background thread or process while training continues; write the manifest when the upload completes. Risks: extra host memory, upload contending with training network traffic, crash before the upload completes (the previous checkpoint stays authoritative), and consistency (the snapshot must be taken at a step boundary).
