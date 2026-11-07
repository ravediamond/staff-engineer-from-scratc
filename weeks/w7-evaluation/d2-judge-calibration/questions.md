# Questions

1. Why κ and not raw agreement?
2. Your two human annotators have κ = 0.55. The judge vs humans has κ = 0.6. Interpret.
3. Name four known LLM-judge biases and a mitigation for each.
4. How big should the calibration set be, and how do you sample it?
5. When should you not use an LLM judge at all?

## Model answers

1. Raw agreement rewards agreeing by chance, which is high when labels are skewed. κ subtracts the agreement expected from the marginals alone: a judge that always says "good" on a 90/10 set gets 90% agreement and κ = 0.
2. The task itself is ambiguous (humans barely agree), so the judge is as good as a human at a noisy task, and the ceiling is the human agreement. Fix the rubric first (clearer criteria, examples, adjudication), re-measure human κ, then the judge. Do not report the judge metric to 3 decimals.
3. Position bias: evaluate both orders and keep consistent verdicts. Verbosity bias: length-controlled comparisons or a rubric penalizing padding; report length alongside. Self-preference: use a judge from a different model family, or an ensemble. Leniency or scale compression: pairwise comparisons instead of absolute scores, anchored rubrics with examples. Sycophancy toward confident wording: rubrics with checkable criteria.
4. 200–500 items for a stable κ (CI about ±0.05–0.1), stratified across slices and score levels, oversampling hard and borderline cases. At least 2 annotators with adjudication. Hold out part of it to validate any judge-prompt tuning.
5. When a deterministic check exists (exact match, unit tests, schema validation, numeric tolerance); when the judge cannot know the answer (domain facts it lacks, private data); for safety-critical final decisions without human review; and when calibration shows κ near human-unreliable levels.
