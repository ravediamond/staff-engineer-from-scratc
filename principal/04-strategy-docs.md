# 4. Writing a technical strategy

Use Richard Rumelt's kernel (*Good Strategy Bad Strategy*), which works for engineering:

1. **Diagnosis:** what is actually going on? The few critical problems, with evidence. ("Each AI team builds its own
   harness and evals; 2 of 3 production regressions last quarter were invisible to their evals; GPU spend grew 3×
   with no utilisation tracking.")
2. **Guiding policy:** the approach that addresses the diagnosis, and what it rules out. ("One shared harness and
   evaluation platform; teams own their datasets and gates; no new team-specific eval frameworks.")
3. **Coherent actions:** the concrete, sequenced steps, owners, and milestones, with measures. ("Q1: shared tracing and
   replay; Q2: eval gates for the top 3 products; Q3: offline↔online tracking; measure regressions reaching users.")

## Template

```
# <Strategy name>   (owner, date, review cadence)
## Diagnosis            evidence, numbers, the 2–3 root problems
## Guiding policy       the approach; what we will NOT do
## Coherent actions     sequenced, owned, measurable (table)
## Bets and risks       what must be true; how we'll know early if we're wrong
## Alternatives         the strategies we rejected and why
## Measures             leading and lagging indicators
```

Bad strategy smells: a list of goals ("be world-class at AI"), a vision with no diagnosis, everything is a priority,
no "will not do" list, no measures.
