# W12 D5: take-home + pair programming + final retro

Paris unicorns often use a take-home or a pair-programming session on a realistic codebase instead of
(or on top of) LeetCode rounds. Today: both, then the 12-week retro.

## Part 1: take-home (4 hours, on a weekend day)

`takehome.md`. Timebox strictly. Submit to yourself as if to a company: a repo, a README, tests.

## Part 2: pair programming (45 min)

`w12d5_pairing.py` is an existing small eval runner, already used by a team. Your pair (imagine the
interviewer) asks for two features: **retry transient errors** (at most 2 retries, only on
`TransientError`), and **per-slice reporting**. Read the existing code first (5 min), ask questions,
then implement in small steps with the tests. Narrate. The review file is a teammate's PR to review in
the last 5 minutes.

## Part 3: final retro (30 min)

Fill the last section of `PROGRESS.md`: per round, your mock score in week 12 vs your first attempt; the
three biggest gaps left; the plan for the next 4 weeks (keep drilling the weakest round, keep the ship log
weekly); and the date you will apply to your first three companies.

## Today's build (`w12d5_pairing.py`)

Existing: `run_case`, `run_all`. Add: `run_case_with_retry`, `slice_report`, and wire both into `run_all(retries=..., by_slice=...)`.
