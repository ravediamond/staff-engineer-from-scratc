# Rubric

Score each line 0 / 1 / 2.

| # | Criterion | Senior signal (1) | Staff signal (2) |
|---|---|---|---|
| 1 | Requirements | "train an RM" | what decisions the RM drives (BoN, DPO, filtering), quality bar, non-goals |
| 2 | Estimation | none | pairs per € (expert minutes per pair), 20–50k pairs year one, compute for RM and DPO, BoN serving cost |
| 3 | Data sourcing | random prompts | real traffic sampled by intent, active selection of uncertain pairs, diverse response generators |
| 4 | Labelling protocol | "experts label" | guidelines + examples, tie/both-bad option, overlap for agreement, gold items, expert time used for hard items only (LLM pre-labels easy ones) |
| 5 | RM training | "fine-tune a model" | prompt-level splits, dedup, ensembles or uncertainty, calibration |
| 6 | RM evaluation | accuracy | held-out accuracy vs human agreement ceiling, slices, calibration, length/style bias probes, adversarial tests |
| 7 | Use of RM | "use it" | BoN with N chosen from gold-vs-N curve, DPO on fresh pairs, KL control, evaluation with independent judges |
| 8 | Hacking detection | none | proxy–gold divergence monitoring, length/style drift, periodic human audits, RM refresh cadence |
| 9 | Verifiable rewards | none | uses checkable signals where they exist (unit conversions, procedure references, tool success) |
| 10 | Scope / sequencing | none | BoN first (no training risk), then DPO, online RL only if justified; success metric |

0–9 senior or below · 10–14 senior+ · 15–17 staff · 18–20 strong staff.
