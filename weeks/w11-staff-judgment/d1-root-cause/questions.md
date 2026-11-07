# Questions (answer with one of YOUR incidents where possible)

1. Tell me about the hardest bug you root-caused. (2 minutes, staff shape: symptom, mechanism, systemic fix, org change.)
2. How do you bisect when the failure is flaky? Quantify.
3. Three teams each say the regression is another team's. How do you run the investigation?
4. What is the difference between a trigger, a root cause and a contributing factor? Example.
5. Write the "why wasn't it caught?" section for an LLM quality regression that reached users.

## Model answers

1. Your own story. Shape: one sentence of impact ("answer accuracy dropped 9 points for French users for 4 days"), two sentences of mechanism ("a tokenizer update changed accent handling; BM25 stopped matching"), one sentence of the systemic fix ("per-language slices in the regression gate"), one sentence of org change ("tokenizer and index changes now go through the eval gate like prompts"), with numbers.
2. Repeat each probe r times and use majority (or a sequential test until confident); size r from the flake rate so the per-check error × log₂(n) checks is acceptable, e.g. a 20% flake needs 5–7 runs for under 5% total error. Also reduce flakiness at the source (seeds, recorded fixtures) before bisecting.
3. Get everyone on shared facts: one timeline, one dashboard, one incident doc. Agree on the symptom metric. Bisect the shared history (deploys, configs, data) with evidence rather than opinions. Assign an owner per hypothesis with a test that would falsify it. Keep it blameless; the deliverable is the systemic fix, not a culprit.
4. The trigger is the event that exposed the problem (a deploy); the root cause is the underlying defect without which it would not happen (a missing language slice, an unvalidated assumption); contributing factors make it worse or slower to detect (no alert on per-language metrics, a holiday on-call gap). Fix all three levels.
5. "The regression gate measured only the global mean; the affected slice was 8% of cases, so a 10-point drop moved the mean by 0.8 points, inside tolerance. No per-language alert existed online. Eval cases for French were 18 months old and did not cover the new feature. Actions: slice gates with Holm correction for top 10 languages, an online per-language quality monitor, quarterly refresh of slice datasets, owner: eval lead, due date."
