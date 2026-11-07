# Questions

1. Kendall τ vs Spearman ρ: what each measures, when to prefer τ.
2. How many past launches do you need to estimate offline↔online agreement usefully?
3. Your offline metric predicts online poorly. Three hypotheses and how to test each.
4. Why write the launch rule as code before the experiment?
5. An executive wants to ship despite an "iterate" decision. What do you say?

## Model answers

1. τ is the probability-like difference between concordant and discordant pairs, easy to interpret ("80% of pairs ordered correctly" ≈ τ = 0.6) and robust with small samples and ties. ρ is the correlation of ranks, sensitive to large rank displacements. With few model versions (5–20), prefer τ.
2. Enough to separate agreement from chance: with 20 launches, 13/20 is not significant; you need about 15/20. Pool across teams and products, and record each launch's offline and online CIs going forward; until then, report the agreement with its CI.
3. The offline set does not represent traffic (compare intent and language distributions to logs); the metric measures the wrong thing (check per-case correlation between metric and user satisfaction signals); online noise or a short duration (check online CIs; the online side may be the noisy one). Also: novelty effects, and judge drift.
4. To prevent motivated reasoning after seeing data (HARKing, metric shopping), to make decisions fast and consistent across teams, and to make overrides visible and accountable.
5. State the facts (effect CI includes zero, guardrails clean, what extra runtime or traffic would resolve it), the risk of shipping (unknown effect, possible slice harm), and options: extend the experiment, ship to a limited segment with monitoring, or ship as a business decision with a named owner and a rollback trigger. The decision is theirs; the record of it is ours.
