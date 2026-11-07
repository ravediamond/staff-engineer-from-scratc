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

The protocol follows the 2025–2026 evidence on learning with AI around (`LEARNING.md`, read it first):
attempt before help, AI as a complement never a substitute, spaced retrieval, AI-off checks.

| Min | Step | File | What you do |
|---|---|---|---|
| 0–5 | Retrieve | `scripts/review.py` | Spaced retrieval: answer due cards out loud before seeing the model answer. Mondays: 10-min delayed recall instead (`LEARNING.md` rule 3). |
| 5–10 | Cold attempt | `predict.md` | Guess BEFORE reading anything. Wrong guesses help (pretesting effect). |
| 10–18 | Read | `README.md` | One page. The concept and the staff angle, nothing more. |
| 18–20 | Check | `predict_run.py` | `uv run python predict_run.py`. Every miss = something you did not understand: one line on why. |
| 20–45 | Build | `wXdY_*.py` | Fill the `TODO`s. `uv run pytest <lab dir> -k "not review"` until green. AI off; debug alone 10 min before any hint. Narrate out loud (W1 D1). |
| 45–53 | Review | `review_*.py` | Code that looks right and is wrong. Find the bug, fix it, write the `WHY:` line. `uv run pytest <lab dir> -k review`. |
| 53–60 | Explain | `questions.md` | Answer out loud, 1–2 minutes each, then `python scripts/review.py add <lab dir>`. Record yourself once a week. |

Plus **15 min drill** (`drills/`), any day you can. From week 5: timed pairs (2 problems, 35 min).
**Friday AI-off gate:** one drill, timer, AI fully off, logged in `PROGRESS.md`.

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
6. **AI is a complement, never a substitute.** Ask it why, never for the code. If you used it to
   generate or debug an exercise, mark ❌ and rebuild from blank within 48 hours.
7. **Green tests today are not learning.** The Monday delayed recall and the Friday AI-off gate are.

## Map

- `LEARNING.md`: how to learn with this repo, from the 2025–2026 research on AI and skill formation
- `CURRICULUM.md`: the 12 weeks, day by day
- `scripts/review.py`: spaced retrieval over every `questions.md` you finish
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
