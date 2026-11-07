# Questions

1. What did you choose as deep dives in each design, and why those?
2. Where did your estimate change the design?
3. What would you do differently with 10 more minutes?

## What good looks like

1. The two riskiest parts for the stated requirements: for the feature store, usually point-in-time correctness or training/serving skew, and online store sizing/latency; for triage, evaluation (label quality, slices) and confidence/abstention (the cost lever). Choosing them yourself, early, is a staff signal.
2. Good answers name a concrete pivot: "unbatched lookups would be 6M reads/s, so the SDK must batch"; "human escalation is 99.7% of cost, so I optimised abstention precision instead of tokens".
3. An honest gap list, not a feature list: e.g. "I never covered backfill cost", "I didn't define the rollback trigger".
