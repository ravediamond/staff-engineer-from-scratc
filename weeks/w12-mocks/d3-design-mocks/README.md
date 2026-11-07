# W12 D3: system design + ML design mocks (2 × 45 minutes)

Two full designs, back to back with a 15-minute break, like a real loop.

1. `system_design.md`: a general system design round (feature store).
2. `ml_design.md`: an ML system design round (LLM support-ticket triage).

Grade each with `rubric.md` (the same 10-line structure as the Friday designs). Model answers are on
`solutions` (`model_answer_system.md`, `model_answer_ml.md`).

The build file is small on purpose: the capacity numbers you need for the two prompts, so you can check
your in-interview arithmetic afterwards.

## Today's build (`w12d3_capacity.py`)

`online_store_size(entities, features, bytes_per_feature, replication)`, `serving_qps(predictions_per_s, features_per_prediction, batch_lookup)`,
`triage_cost_per_month(tickets_per_day, in_tokens, out_tokens, usd_in, usd_out, escalation_rate, usd_per_human_ticket)`.
