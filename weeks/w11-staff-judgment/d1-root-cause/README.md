# W11 D1: root cause

> **Full lesson for this day:** [`../README.md`](../README.md#day-1-root-cause) (the week page: concepts from zero, examples, traps).
> This file is the one-page summary with the staff angle. Order of work: `predict.md` → the lesson → `predict_run.py` → the exercise → the review file → `questions.md`.

Primer: `knowledge/12-staff-rubrics.md` §3 ("Fix root causes").

## The one idea

Root-causing is a search problem with noisy oracles. Three tools cover most incidents:

1. **Bisect** over an ordered history (commits, configs, model versions, data snapshots): log₂(n)
   checks instead of n. With a **flaky** check, one run is not evidence: run it r times, take the
   majority, and say the error rate of your procedure.
2. **Change-point detection** on a metric: where did it leave its baseline? Today: the first point
   above `mean + k·std` of a baseline window. Crude, explainable, often enough.
3. **Correlate with events**: the last deploy / config push / data refresh at or before the change
   point. Correlation is a lead, not a verdict: confirm by reverting or reproducing.

The staff habit is writing the chain down: symptom → mechanism → trigger → why it was possible →
why it wasn't caught. The last two are where the fix that prevents the next ten incidents lives.

## Today's build (`w11d1_rootcause.py`)

`bisect_first_bad(n, is_bad, repeats)` → `(index, checks)`, `majority(results)`, `change_point(series, baseline_n, k)`,
`last_event_before(t, events)`.

## Staff angle

In interviews, the "tell me about a hard bug" question is a staff question in disguise. Seniors tell
the debugging. Staff tell the debugging in two sentences, then the systemic fix ("we added a canary
eval that would have caught it, and it caught three more since"), then what they changed in how the
org works. Prepare that shape for two of your own incidents.
