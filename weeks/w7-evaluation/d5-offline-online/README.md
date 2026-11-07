# W7 D5: offline ↔ online agreement, launch rules + Friday design

Primer: `knowledge/07-evaluation-and-experimentation.md` §5.

## The one idea

An offline metric is only worth what it predicts online. Measure that directly, across
past launches:

- **Rank correlation** between offline and online scores of model versions: **Kendall τ** (pairs
  ordered the same way minus pairs ordered differently, over all pairs) and **Spearman ρ** (Pearson
  correlation of ranks, ties get average ranks).
- **Sign agreement** on deltas: of the past launches, how often did the offline delta and the
  online delta have the same sign? If it is 60%, your offline eval is barely better than a coin flip.

**Launch rule** as code: written before the experiment, so nobody argues after.

## Today's build (`w7d5_offline_online.py`)

`kendall_tau(x, y)` (tau-a), `average_ranks(x)`, `spearman(x, y)`, `sign_agreement(pairs)`,
`launch_decision(offline_ci, online_ci, guardrail_breaches)` → `"ship" | "iterate" | "rollback"`.

## Friday design (45 min)

`design.md`: evaluation infrastructure for an AI product with 30 teams. Timer, `my_design.md`,
`rubric.md`, model answer on `solutions`.

## Staff angle

The most valuable chart an eval lead can show leadership is "offline delta vs online delta, for
every launch in the last year". It answers "can we trust our evals?" with data, tells you which
offline metric to retire, and turns evaluation from a cost centre into a decision system.
