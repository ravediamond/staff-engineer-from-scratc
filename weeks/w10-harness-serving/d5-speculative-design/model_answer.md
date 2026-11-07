# Model answer: agentic coding assistant (staff level)

## 1. Requirements
In scope v1: bug fixes with a reproducible failing test, small features in well-tested services,
dependency bumps, test additions. Success = PR merged without major rework and not reverted within 30
days. Safety: the agent never pushes to protected branches, never merges, has no production
credentials, cannot exfiltrate code. Non-goals: architecture changes, cross-repo migrations, infra changes.

## 2. Estimation
2,000 engineers, ~10% adoption at start → 200 tasks/day. Per task: ~40 steps, ~600k input tokens
(with prompt caching), ~40k output → ~$3–8 per task at frontier-model prices; sandbox ~20 min of a
4-vCPU VM ≈ $0.10. 200 tasks/day ≈ $30k/month. Worth it if it saves >1 engineer-hour per merged PR.

## 3. Architecture
Ticket intake → planner step (reads ticket + repo map) → harness loop with tools: search code, read
file, edit (diff-based), run command (policy-checked), run tests, open PR. Sandbox: ephemeral microVM per
task with the repo checked out, dependency caches, no secrets; egress allow-list (package mirrors only);
a short-lived token scoped to "push branch + open PR" held by the PR tool, not the shell. Every run traced
(W10 D3); the PR description links to the trace and lists the verification evidence.

## 4. Deep dives
**Verification ("prove it works"):** the harness requires, before "done": the failing test reproduced
before the change (for bug fixes), passing after; full relevant test suite, linter and type checks green;
diff limited to the files the plan named (larger diffs need justification); no test files weakened
(diff check on assertions and deleted tests). Missing evidence → run marked "needs human", not "done".
**Evaluation:** offline: 500 historical tickets with their real fixes and hidden tests (the tests the
human added), sliced by repo, language and task type; metric = hidden tests pass + reviewer-rubric
score on a sample; paired comparison for every harness or model change, with CIs (W7). Online: staggered
rollout by team; metrics = merge rate, review time per PR, revert rate within 30 days, time from ticket
to merge vs matched tickets done by humans in the same teams (difference-in-differences); engineer survey
as secondary. Guardrails: revert rate, security findings, cost per merged PR.

## 5. Metrics, risks, scope
Month-one failure modes: editing tests to pass, wandering diffs, flaky tests misread as failures,
prompt injection via repo content (e.g. a comment instructing the agent), cost blow-ups on long loops.
Mitigations in the harness: test-tamper checks, diff budgets, flake detection by re-running, treating
repo text as untrusted, per-task budgets. Rollout: two volunteer teams, bug-fix tasks only, then expand by
task type as offline and online metrics clear their bars.
