# Questions

1. Prove (sketch) that speculative decoding preserves the target distribution.
2. When does speculative decoding help and when does it not?
3. Draft model options besides a smaller model of the same family.
4. In your coding-assistant design, what is the single most important harness invariant, and why?
5. What did you put in your own skill set's principles, and which one would you defend first in an interview?

## Model answers

1. For a drafted x ~ q: P(output = x via acceptance) = q(x)·min(1, p(x)/q(x)) = min(q(x), p(x)). Rejection happens with probability 1 − Σ min(p, q), and the residual distribution is (p − min(p, q)) / (1 − Σ min(p, q)). Total: min(p, q) + (p − min(p, q)) = p(x). Induction over positions gives the joint distribution.
2. It helps when acceptance is high (predictable continuations: code, structured output, repetitive text), the draft is much cheaper, and serving is latency-bound at low batch with spare compute. It helps less at high batch (the target is already efficient per token, verification steals batch capacity), with low acceptance (creative text, mismatched draft), or under memory pressure (the draft's own KV cache).
3. N-gram or prompt-lookup decoding (copy from context), Medusa or EAGLE heads on the target model itself (no separate model), self-speculation with early-exit layers, or a quantized version of the target.
4. "No claim of done without verification evidence": tests reproduced and passing, checks green, diff within plan, all attached to the PR. It converts the model's confidence into evidence a reviewer can check quickly, which is what makes the time savings real and the trust durable.
5. Your own answer. A strong one names a principle, the incident or project that taught it, and a mechanism enforcing it (a test, a gate, a checklist), e.g. "Paired comparisons only: I once approved a prompt change on an unpaired comparison and shipped a 3-point regression; our gate now refuses unpaired results."
