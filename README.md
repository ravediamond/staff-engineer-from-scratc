# Staff Engineer From Scratch

12 weeks. 1 hour a day, Monday to Friday. Goal: become, for real, a staff engineer in
**ML/AI systems** on a **solid general-SWE base**, and pass the full staff loop at Google (L6),
Meta (E6) and Paris unicorns (Mistral, Hugging Face, H, Dust, Photoroom, Poolside, Alan, Doctolib…).

Specialty: **harness engineering, RAG, evaluation, reward models, distributed training infrastructure.**

The bar is not "pass a loop". The bar is the engineers you read about (Lauren Tan, author of
pstack, is the reference): rigor, verification before claims, written judgment, and shipping
in public. A loop is just the visible checkpoint.

No GPU needed. Every lab runs on a Mac (CPU) in under 5 minutes. Weeks 8 and 9 use PyTorch
(CPU, `gloo` backend for the distributed labs).

## Setup (once)

```bash
uv sync                                         # numpy, torch, pytest
uv run pytest weeks/w1-coding-base/d1-heap      # should FAIL: you have work to do
```

## A day (1 hour)

| Min | Step | File | What you do |
|---|---|---|---|
| 0–10 | Read | `README.md` | One page. The concept and the staff angle, nothing more. |
| 10–15 | Predict | `predict.md` → `predict_run.py` | Write your guesses in `predict.md` FIRST. Then `uv run python predict_run.py` and compare. Every miss = something you did not understand. Write one line on why. |
| 15–45 | Build | `wXdY_*.py` | Fill the `TODO`s. `uv run pytest <lab dir> -k "not review"` until green. Narrate out loud while coding (W1 D1 explains the protocol). |
| 45–55 | Review | `review_*.py` | Code that looks right and is wrong. Find the bug, fix it, write a one-line explanation at the top of the file. `uv run pytest <lab dir> -k review` turns green when fixed. |
| 55–60 | Explain | `questions.md` | Answer out loud, as in an interview. 1–2 minutes each. Record yourself once a week. |

Plus **15 min drill** (`drills/`), any day you can. From week 5: timed pairs (2 problems, 35 min).

Plus, **once a week, 20 min reading slot** (`reading/`): one real file from a real system (vLLM,
PyTorch DDP, TRL, lm-eval-harness, etcd Raft, pstack…), read only, 10-line note.

Plus, **once a week, ship one public thing** (`SHIPLOG.md`): a post, a skill, an OSS PR, a lab write-up.
The labs train you. The ship log makes you the person.

On 2-hour days: delete your solution and redo the lab from a blank file, no notes.
Then read the week's knowledge primer (`knowledge/`).

## Friday designs (weeks 5–10)

Each Friday of weeks 5 to 10 has a `design.md`: a 45-minute written design of that week's
platform, timed, then graded against `rubric.md`. A model answer is on the `solutions` branch.
Read it only after you graded yourself.

## Rules

1. **No AI in exercise files.** The repo's `CLAUDE.md` puts Claude in tutor mode: hints and questions only.
   Stuck 10 minutes: ask for a hint, not code.
2. **Predict before you run.** Always.
3. **Say the invariant.** Every non-trivial function gets a one-line invariant comment
   (`# invariant: heap[i] <= heap[2i+1]`). Staff engineers think in invariants.
4. **Solutions are on the `solutions` branch.** Look only after the tests are green, or after 20 minutes
   truly stuck. `git diff master solutions -- <file>` shows one file.
5. **Tick `PROGRESS.md`** at the end of each session. Honest marks only.

## Map

- `CURRICULUM.md`: the 12 weeks, day by day
- `weeks/`: the 60 labs
- `drills/`: 48 interview problems with tests, 4 per week
- `knowledge/`: 15 dense primers with interview questions (the discussion rounds)
- `principal/`: the staff → principal playbook (what changes, how it is judged, exercises)
- `reading/`: the weekly read-only slot
- `private-template/`: the format of your private material (STAR bank, case files). Your real
  material lives in a separate private repo and is synced into `reference/your-work/` (gitignored)
  by `scripts/sync_private.sh`. Never commit employer material to this public repo.
- `SHIPLOG.md`: one public artifact per week
- `PROGRESS.md`: your tracker

## Why these three skills

| Skill | Interview round it trains | Daily-life use |
|---|---|---|
| Build | "Implement X in 35 minutes", take-homes, pair programming | Write the code instead of delegating it |
| Predict | "What happens if…", estimation, design trade-offs | Know what a result should look like before it arrives |
| Review | "This code/design is broken, find it", code review signal | Catch generated code, catch your team's bugs, catch your own |

## The staff signal, in one table

| Level | Owns | Judged on |
|---|---|---|
| Senior | a feature, a service | correct, clean, on time |
| Staff | a problem space across teams | direction set, ambiguity removed, others made faster, outcomes measured |
| Principal | a technical bet for the org | the bet was right, years later; the org changed how it works |

Every lab README ends with a **Staff angle** paragraph: what a staff engineer would say in that
discussion that a senior would not.
