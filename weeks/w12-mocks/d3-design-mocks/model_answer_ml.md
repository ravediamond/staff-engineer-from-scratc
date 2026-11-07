# Model answer: LLM ticket triage (staff level)

**Requirements.** Classify into 140 categories, set priority, route; draft a reply for the ~30% of
tickets that are known how-to questions; abstain and escalate when unsure. Success: routing accuracy ≥
human baseline (measure it: humans disagree too), time-to-first-response down, agent workload down,
no increase in reopen rate or SLA breaches. Non-goals v1: fully automated replies without review for
enterprise customers.

**Estimation.** 50k/day ≈ 0.6/s average, peaks ~5/s: latency budget is generous (seconds). LLM cost
≈ $4k/month at small-model prices; human handling ≈ $1.5M/month: **the escalation rate is the cost
lever**, not tokens. Every point of safe automation is worth ~$60k/month.

**Design.** Ingest → language detection → retrieval of similar resolved tickets and KB articles →
classifier: a fine-tuned small model or an LLM with few-shot retrieved examples outputting category +
priority + calibrated confidence → routing rules (customer tier, SLA) → reply drafter (RAG over KB,
citations) for eligible categories → confidence gate: auto-route above threshold, human review below.
Agents' corrections are logged as labels.

**Deep dive: evaluation.** Offline: 5k historical tickets relabelled by 2 senior agents (measure their
agreement: taxonomy ambiguity is the accuracy ceiling), sliced by language, category frequency and
customer tier; metrics: top-1/top-3 accuracy, macro-F1 (rare categories matter), priority confusion
(critical misses weighted heavily), calibration (ECE) for the gate. Online: shadow mode for 2 weeks (model
predicts, humans decide, compare), then staggered rollout with guardrails (reopen rate, SLA breaches,
CSAT), A/B by queue.

**Deep dive: confidence and abstention.** Calibrate confidence (temperature scaling on held-out data,
W8 D3); choose per-category thresholds from accuracy-vs-coverage curves to hit the target precision
(e.g. 97% for routing, 99% for critical priority); critical-priority predictions always get a human
check. Taxonomy drift: track the "other/unsure" rate and agent corrections per category; quarterly
taxonomy review; new categories bootstrap from agents' labels.

**Ops and scope.** Feedback loop: weekly retraining or example-set refresh from corrections, gated by the
offline suite. Monitoring per language and category. Not in v1: autonomous replies, sentiment-based
priority beyond the classifier. Build vs buy: helpdesk vendor AI features vs own; own if the taxonomy and
routing logic are differentiating and volume justifies it.
