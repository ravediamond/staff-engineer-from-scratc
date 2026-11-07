# Questions

1. What goes into a trace for an agent run? Sketch the span tree.
2. How does deterministic replay work, and what makes it hard with LLMs?
3. How would you use replay to test a prompt change against production behaviour?
4. Traces contain user data. How do you store them responsibly?
5. How do you attribute cost per feature/team from traces?

## Model answers

1. Run span (user, agent version, config, budget) → step spans → model-call spans (model, params, tokens in/out, latency, finish reason, the prompt and response or references to them) and tool-call spans (tool, canonical args, output or a truncated reference, status, retries) → nested spans for retrieval, sub-agents and so on. Plus run-level outcome (status, answer, feedback).
2. Record every external interaction (tool outputs, and model outputs if you want full determinism) and serve them back by position, checking arguments. Hard parts: model sampling is non-deterministic (record model outputs, or replay only tools and accept model variation); hidden inputs (time, randomness, environment) must also be recorded; long traces make the first divergence cascade.
3. Take a stratified sample of recorded production traces; re-run the new prompt with tools replayed from recordings; for runs that diverge (ReplayMismatch), either stop and inspect the divergence or switch to a sandboxed live mode; score final answers with the eval suite; compare against the original outcomes with paired statistics.
4. PII redaction or tokenization at ingestion where possible, encryption at rest, access control by role with audit logs, retention limits, sampling (keep 100% of metadata, a fraction of payloads), customer opt-outs and data residency, and a separate, consented dataset for eval use.
5. Tag runs with feature, team and customer at the entry point (propagated as trace attributes), sum model-span tokens × prices plus tool costs per tag, and reconcile with provider bills. Publish cost per successful task, not just per call.
