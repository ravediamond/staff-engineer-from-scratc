# Mock system design (45 min): a feature store

Design a feature store for a company with 40 ML models in production (fraud, recommendations, pricing,
search ranking). Requirements gathered so far: features computed in batch (daily) and streaming
(seconds); online serving at 20k predictions/s with p99 < 10 ms for feature retrieval; point-in-time
correct training datasets; 200M entities; feature reuse across teams.

The interviewer will push on: training/serving skew, point-in-time correctness, the online store choice
and its sizing, backfills when a feature definition changes, and ownership/governance.
