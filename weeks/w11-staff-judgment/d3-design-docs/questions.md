# Questions

1. Walk me through the structure of a design doc you wrote. What was decided, and what changed because of it?
2. Why are non-goals the most valuable section?
3. How do you get a doc reviewed and decided in under two weeks across four teams?
4. Two senior engineers disagree strongly in the doc comments. What do you do?
5. When should you NOT write a design doc?

## Model answers

1. Your own doc: context with a number, the 2–3 options and the trade-off table, the decision and the deciding factor, and the outcome measured against the doc's metrics, including what you got wrong.
2. They prevent scope creep, make disagreement explicit early ("you assumed we'd also migrate X: we won't"), protect the timeline, and tell readers which concerns are deliberately parked rather than forgotten.
3. Pre-wire: talk to each team's key reviewer before publishing. Publish with a clear decision deadline and named approvers (DACI/RACI). Separate "must resolve" from "nice to discuss" comments. Hold one focused review meeting on the open questions only. Record the decision and dissent in the doc.
4. Restate both positions until each agrees you got theirs right, find the underlying assumption that differs (usually a requirement or a number), and resolve it with data or a cheap experiment if possible. Otherwise escalate to the decider with a fair summary and a recommendation. Disagree-and-commit is explicit and recorded.
5. When the change is small and reversible, when the team already agrees and a short PR description or ADR suffices, or when a prototype would answer the question faster than prose. Doc length should scale with blast radius and irreversibility.
