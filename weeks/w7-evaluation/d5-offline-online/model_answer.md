# Model answer: evaluation platform (staff level)

## 1. Requirements
Every change (prompt, tool, retrieval, model, config) gets an eval report on its PR in < 30 min;
blocking gates for critical datasets; coverage of top 10 markets and top intents; reproducible runs
(same inputs → same report); online experiment integration for model-level changes. Non-goals v1:
training-data curation, red-teaming platform (separate), real-time production monitoring (reuse
observability stack, link to it).

## 2. Estimation
Core suite: 2,000 cases × 3 repeats = 6k calls per run; with judge calls ≈ 12k calls; at ~$0.005 per
call ≈ $60 per full run. 40 changes/week × ~3 runs each ≈ 120 runs ≈ $7k/week; with caching of
unchanged components and a smart subset for drafts ≈ $3k/week. Cheaper than one regression.

## 3. Data model
Dataset (name, version, owner, slices, provenance, refresh date), Case (id, input, references,
slice tags, rubric), Run (dataset version, system fingerprint = hashes of prompts/tools/model/config,
seed, repeats), Result (case id, outputs, scores per metric, judge rationale), Comparison (base run,
new run, stats). All immutable and addressable by id.

## 4. Architecture
CI hook → eval service schedules a run on a distributed runner (queue + workers with rate limits per
provider) → system under test runs with recorded tool fixtures (or a sandboxed live mode) → scorers
(deterministic checks first, calibrated judges second) → stats service (paired bootstrap, slice gates,
Holm) → report on the PR (summary, failing slices, diff view of the worst 20 cases) → results store
feeding dashboards. Online: model-level changes go to the A/B platform with standard guardrails;
results flow back into the same store for offline↔online analysis.

## 5. Deep dives
**Judges you can trust:** a 400-item calibration set per judge task, 2 annotators + adjudication,
human κ reported; judge prompt changes require recalibration; judge κ vs humans shown next to the
metric; pairwise judgments run in both orders; length reported alongside quality.
**Gating 40 changes/week without becoming the bottleneck:** tiered suites (smoke: 200 cases in 5 min
on every commit; full: on PR ready; extended: nightly). Gate rule pre-registered: block on a
significant regression on critical datasets/slices, warn otherwise. Owners for each dataset, an
override needs the owner's approval with a written reason. Weekly eval review: overrides, flaky
cases, new cases from incidents.

## 6. Metrics and process
Platform metrics: regressions reaching users per month (target: 0 in critical slices), time-to-report,
cost per run, flaky case rate, offline↔online sign agreement over launches (target > 80%, reviewed
quarterly; metrics that do not predict online get retired). Rollout: three teams with the most
regressions first, shadow gates for 4 weeks, then blocking. Not built in v1: synthetic data
generation service, custom labelling tool (buy).
