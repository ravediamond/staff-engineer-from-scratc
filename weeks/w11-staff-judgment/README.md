# Week 11: Staff judgment

**Everything you need for this week is on this page.** You need the earlier weeks as material (idempotency and versions from weeks 2 and 6, evaluation from week 7). Plain Python. Nothing from other folders is required to do the labs; Wednesday and Friday also ask you to write about your own work, privately.

Coding and design rounds check that you can build. The level you are hired at is decided by something else: how you find the real cause of a problem, how you prove a claim, how you write a decision down so that others can act on it, how you change a live system without breaking it, and how you tell what you did. These are the five days of this week. Each one has a small build, because a habit you can turn into a tool is a habit you actually have.

## Start here

1. Read [The week in one table](#the-week-in-one-table) and [What changes at staff level](#what-changes-at-staff-level).
2. Each day, open that day's folder and follow [What to do each day](#what-to-do-each-day).
3. The lesson for each day is the matching section of this page: [Day 1](#day-1-root-cause), [Day 2](#day-2-prove-it-works), [Day 3](#day-3-design-documents), [Day 4](#day-4-live-migrations), [Day 5](#day-5-your-stories-as-data).
4. Friday: [End of the week](#end-of-the-week).

### What is in a day folder

| File | What it is | You |
|---|---|---|
| `predict.md` | small questions, answered before you read anything | write guesses |
| `README.md` | one-page summary of the day, with its "staff angle" | read after the lesson |
| `predict_run.py` | prints the real answers | run, compare |
| `w11dN_*.py` | **the exercise**, with `# TODO` | **write the code** |
| `test_w11dN_*.py` | tests | run, never edit |
| `review_w11dN.py` + its test | code with one planted bug | **find and fix**, write the `WHY:` line |
| `questions.md` | interview questions | answer out loud |

Wednesday and Friday produce private files (`my_rfc.md`, `stories.json`). Anything that describes your employer's systems stays out of this public repo: see Friday.

### What to do each day

One hour, commands from the repo root.

| Min | Step | Command or file |
|---|---|---|
| 0–5 | Retrieve (Monday: 10-min delayed recall of last week's hardest function instead) | `uv run python scripts/review.py` |
| 5–10 | Guess, before reading | `predict.md` |
| 10–18 | Read the lesson | the day's section on this page |
| 18–20 | Check your guesses | `uv run python weeks/w11-staff-judgment/<day>/predict_run.py` |
| 20–45 | Build, narrating out loud | `uv run pytest weeks/w11-staff-judgment/<day> -k "not review"` until green |
| 45–53 | Review | `uv run pytest weeks/w11-staff-judgment/<day> -k review` |
| 53–60 | Explain | `questions.md` out loud, then `uv run python scripts/review.py add weeks/w11-staff-judgment/<day>` |

Guess before reading even if you know nothing: a wrong guess makes the lesson stick (`LEARNING.md` rule 1). AI stays off in the exercise files; stuck for 10 minutes, ask for a hint, not code.

## The week in one table

| Day | Folder | The habit | You build | The review bug is about |
|---|---|---|---|---|
| Mon | `d1-root-cause` | fix causes, not symptoms | bisection with a flaky check, change-point detection, event correlation | what the search returns |
| Tue | `d2-prove-it-works` | prove it works | a small property-based testing engine with shrinking | what is reported after shrinking |
| Wed | `d3-design-docs` | write decisions down | a linter for design documents; then your own RFC | what counts as a heading |
| Thu | `d4-migrations` | change live systems safely | a resumable backfill, a verifier, a migration state machine | when the cut-over is allowed |
| Fri | `d5-star-bank` | tell your work at the right level | validation, coverage and retrieval for your stories | which stories are counted |

## What changes at staff level

| Level | Owns | Judged on |
|---|---|---|
| Senior | a feature, a service | correct, clean, on time |
| Staff | a problem that spans teams | direction set, ambiguity removed, others made faster, outcomes measured |
| Principal | a technical bet for the organisation | the bet was right, years later |

A senior engineer is given a problem and solves it well. A staff engineer is given a **situation** and has to decide what the problem is, convince other teams, and leave behind something that works without them. Interviewers look for that in everything: which questions you ask, whether you state what you will **not** do, whether you measure, whether your stories are about a task or about a decision.

Two phrases you will meet: **scope** (how many people and systems your work changed) and **ambiguity** (how undefined the problem was when you took it).

## Day 1: Root cause

Folder: `d1-root-cause`. Exercise: `w11d1_rootcause.py`.

### Finding a cause is a search

Something broke. There is a long list of things that changed. Checking them one by one is slow, and guessing is how teams "fix" the same incident three times. Three tools cover most cases.

### Tool 1: bisection

The history is **ordered**: commits, configuration versions, model versions, data snapshots. Version 0 is known to be good, the last one is known to be bad. Test the middle. If it is bad, the first bad version is in the first half; if good, in the second. Each test halves the range: about `log₂(n)` tests for `n` versions. A thousand commits, ten tests.

The search ends when the good side and the bad side are next to each other, and the answer is the **boundary**: the first bad version. Returning the last midpoint tested gives a version near the culprit and often not the culprit. That is today's review bug.

It relies on one assumption: once bad, always bad after that.

**A flaky check.** Real checks sometimes give the wrong answer: a test that fails one time in ten for unrelated reasons. One run is then **not evidence**. A single wrong answer sends the search into the wrong half, and it finishes, confidently, on an innocent commit. Run the check several times at each point and take the **majority**. More repeats, more cost, fewer wrong conclusions. Say the error rate of your procedure when you report the result.

```python
votes = [True, False, True]
sum(votes) > len(votes) / 2            # True: strictly more than half
```

### Tool 2: change-point detection

A metric was steady and then was not. **When** did it leave its baseline? Today's method is the simplest one: take the mean and the standard deviation of a baseline window at the start, and find the first later point above `mean + k × standard deviation`.

```python
import statistics
base = [10, 11, 9, 10, 10]
statistics.mean(base) + 3 * statistics.stdev(base)       # 12.1: the alarm line for k = 3
```

Crude, and explainable to anyone in an incident channel, which is worth more than a clever method nobody trusts at 3 a.m.

### Tool 3: correlate with events

With a time in hand, look for the last deploy, configuration push or data refresh **at or before** it. In a sorted list of events that is a binary search (`bisect`, week 1).

A correlation is a **lead**, not a verdict. Confirm it by reverting the change or by reproducing the failure. "The deploy was just before" has sent many teams after the wrong change.

### The written chain

The staff habit is to write the chain down:

```
symptom → mechanism → trigger → why it was possible → why it was not caught
```

Most post-mortems stop at the trigger ("a bad configuration was pushed"). The last two links are where the fix that prevents the next ten incidents lives: a missing validation, a missing alert, a missing test.

### Traps of the day

- One run of a flaky check.
- A tie in the vote counted as a majority.
- The baseline window including the anomaly.
- An event **after** the change point named as the cause.

### Today's build

| Function | Job | Lesson section |
|---|---|---|
| `majority` | strictly more than half | a flaky check |
| `bisect_first_bad` | first bad version and the number of checks used | bisection |
| `change_point` | first point above the baseline band | change-point detection |
| `last_event_before` | the last event at or before a time | correlate with events |

Run: `uv run pytest weeks/w11-staff-judgment/d1-root-cause -k "not review"`

---

## Day 2: Prove it works

Folder: `d2-prove-it-works`. Exercise: `w11d2_pbt.py`.

### Beyond the examples you thought of

An ordinary test checks specific cases: "`dedupe([1, 1, 2])` is `[1, 2]`". It only covers what you imagined, and bugs live in what you did not imagine.

A **property-based test** states something that must hold for **every** input, and lets the machine look for a counterexample among hundreds of random inputs.

For a function that removes duplicates from a sorted list, three properties: the output is sorted; it has no duplicates; it contains the same set of values as the input. No expected output is written by hand.

Typical kinds of properties:

| Kind | Example |
|---|---|
| invariant | the output of a sort is ordered |
| round trip | `decode(encode(x)) == x` |
| idempotence | applying it twice equals applying it once |
| comparison with a simple reference | the fast version equals the slow, obvious one |

The last kind is the test of week 9: a distributed run equals a single process.

### Generators

A **generator** produces a random input from a seeded random source: an integer in a range; a list of random length whose elements come from another generator. Seeded, so that a failure can be reproduced.

```python
import random
rng = random.Random(0)
[rng.randint(-5, 5) for _ in range(rng.randint(0, 6))]       # one random list
```

### Shrinking

A random counterexample is noise: `[-83, 17, 17, 902, -4, 55, 55, 55, 3]`. Somewhere in it is the two-element input that really shows the bug. **Shrinking** finds it.

Greedy shrinking: from a failing input, generate **smaller candidates**. Move to the first candidate that **still fails**. Repeat from there. When no candidate fails, the current input is a local minimum: return it.

| Type | Smaller candidates, in order |
|---|---|
| an integer `x` | 0; `x` halved toward zero; one step closer to zero |
| a list | the empty list; its first half; its second half; the list with one element removed, for each position; the list with one element shrunk, for each position and each candidate |

Candidates equal to the input itself are left out, or the search never ends. Halving toward zero means `int(x / 2)`: `-7` gives `-3`. (`-7 // 2` is `-4` in Python, which also works toward zero slowly but is not what the docstring asks.)

The result is usually the bug report itself: "fails on `[0, 0]`".

The search keeps going until **no** candidate fails, and what it returns is the **last failing input it reached**. Returning the original input after doing all that work is today's review bug: the report then shows the noisy case, and the minimal one is lost.

### "Prove it works" as a habit

Before saying "done": what would convince a sceptical colleague? A test that fails without the change and passes with it. A property over random inputs. A comparison with a reference. A number with an interval (week 7). It is the first principle of the engineer this repo takes as a model, and the habit that makes people trust your claims without checking them.

### Traps of the day

- The original input reported instead of the minimised one; shrinking that stops after one step.
- The input itself among its own candidates.
- A generator without a seed: the failure cannot be reproduced.
- A property that restates the implementation: it passes whenever the code runs.

### Today's build

| Function | Job | Lesson section |
|---|---|---|
| `gen_int`, `gen_list` | random inputs from a seeded source | generators |
| `shrink_int`, `shrink_list` | smaller candidates, in the stated order | shrinking |
| `minimize` | greedy descent to a minimal failing input | shrinking |
| `check` | run a property on `n` inputs; return `None` or the minimised counterexample | beyond the examples |

Then point your engine at the provided `dedupe_sorted_buggy` and read what it finds.

Run: `uv run pytest weeks/w11-staff-judgment/d2-prove-it-works -k "not review"`

---

## Day 3: Design documents

Folder: `d3-design-docs`. Exercise: `w11d3_doclint.py`.

### Why a document

At staff level your most leveraged output is often not code. It is the **design document** (also called an RFC, request for comments): the text that turns a debate into a decision other people can carry out without you. A good one is read by ten people, saves weeks of meetings, and still explains, a year later, why things are the way they are.

### The skeleton

| Section | Must contain |
|---|---|
| Context | the problem in the **reader's** terms, with one number |
| Goals | 3 to 5, measurable |
| **Non-goals** | what you deliberately will not do |
| Proposal | the design, with one request walked from end to end |
| **Alternatives considered** | at least two real options, each with why not |
| Risks | what could go wrong, and the mitigation |
| Rollout | phases, flags, how to roll back |
| Metrics | how you will know it worked: numbers, not adjectives |

**Non-goals** is the most skipped section and the most valuable. It stops the review from drifting to everything the design could also do, and it shows that the scope was chosen.

**Alternatives** show that the proposal was a choice. "Do nothing" and "keep the status quo" are worth mentioning as a baseline, and they do **not** count as alternatives: a document whose only other option is to do nothing has considered no alternative.

### A linter for the skeleton

A tool cannot judge whether a design is good. It can check that every section exists and is not empty, that there are at least two alternatives, that the metrics contain a number. That removes the mechanical part of a review and leaves the reviewers' time for the content.

The linter works on Markdown:

- Remove fenced code blocks first: a line starting with `##` inside a code block is not a heading. Counting those as sections is today's review bug: a document that shows a Markdown example then appears to have sections it does not have.
- A section is a line starting with `## ` and everything up to the next one. `### ` subheadings stay inside their section.
- Alternatives are counted as `### ` subheadings when there are any, otherwise as top-level bullets.

```python
import re
fence = "`" * 3                                               # three backquotes
md = "## Goals\n- fast\n" + fence + "\n## not a heading\n" + fence + "\n## Risks\nnone"
re.sub(fence + ".*?" + fence, "", md, flags=re.S).count("## ")     # 2: the fenced block is gone
```

### After the tests pass: your own RFC

Write a real design document, `my_rfc.md`, for a problem you own, and make it pass your linter. If it contains anything about your employer's systems, it does not go into this public repo (see Friday for where private files live).

### Traps of the day

- Headings inside code blocks counted as sections.
- "Do nothing" counted as an alternative.
- A section that exists and is empty reported as fine.
- Issues reported in an order other than the docstring's: the tests compare lists.

### Today's build

| Function | Job | Lesson section |
|---|---|---|
| `strip_code_blocks` | remove fenced blocks | a linter for the skeleton |
| `sections` | `{title: body}` for `## ` headings | a linter for the skeleton |
| `count_alternatives` | real options only | the skeleton |
| `lint` | the list of issues | the skeleton |

Run: `uv run pytest weeks/w11-staff-judgment/d3-design-docs -k "not review"`

---

## Day 4: Live migrations

Folder: `d4-migrations`. Exercise: `w11d4_migration.py`.

### The problem

Move a system that is in use (to a new database, a new schema, a new embedding model, a new feature store) with no downtime and no lost data. People read and write the whole time. It is a staff rite of passage, and a favourite interview question because there is one right shape.

### The six phases

```
dual write → backfill → verify → cut over reads → stop old writes → clean up
```

| Phase | What happens | Reads come from |
|---|---|---|
| **dual write** | every write goes to the old store **and** the new one. From this moment, new data is in both. | old |
| **backfill** | copy the history from old to new | old |
| **verify** | compare old and new; the mismatch rate must be under a threshold | old |
| **cut over reads** | reads move to the new store, behind a flag. **Writes still go to both.** | new |
| **stop old writes** | the old store stops receiving writes and starts going stale | new |
| **clean up** | remove the old store and the dual-write code | new |

**Invariant:** at every moment one store is fully correct, and reads come from it.

**Rollback** is possible, and instant, at every phase up to and including the read cut-over: the old store is still receiving every write, so it is still correct; flip the flag back. After old writes stop, the old store is stale and there is no way back. That asymmetry is why the phases are in this order, and why nobody stops old writes on the day of the cut-over.

### The backfill

It copies history while live writes continue. Four properties:

- **Ordered and batched**: keys in sorted order, a limited number per call.
- **Resumable**: it returns a **checkpoint**, the last key it processed. The next call starts **after** that key. A backfill that has to restart from zero after each crash never finishes on a large store.
- **Idempotent**: copying a key twice changes nothing.
- **Version-aware**: this is the subtle one. While the backfill runs, dual writes put **newer** values into the new store. The backfill reads an older value from the old store a moment later and must not write it over the newer one. So every record carries a version, and the backfill writes only if the new store has nothing for that key or an older version.

A backfill that overwrites blindly silently reverts recent writes. It is a real cause of data loss in migrations.

### Verification

Compare the stores key by key (or on a large sample). A key is a **mismatch** if it is missing from the new store, if the new store has a **lower** version, or if the versions are equal and the values differ. The new store being **ahead** is not a mismatch: dual writes can land there first.

The mismatch rate is compared with a threshold decided in advance. The cut-over is allowed only with that evidence. A migration that lets reads move to the new store before verification has passed is today's review bug: it serves users from a store nobody has checked.

### The state machine

The migration is an object that knows its phase. `advance` moves to the next phase only when it is given the evidence that phase requires (a finished backfill, a mismatch rate under the threshold) and refuses otherwise. `rollback` is refused once old writes have stopped. `read_from` answers "old" or "new" from the phase.

Encoding the procedure as a state machine makes the dangerous shortcuts impossible to take by accident, which is the point.

### Traps of the day

- A backfill that overwrites newer versions.
- A checkpoint that restarts **at** the last key instead of after it, or skips one.
- "New is ahead" reported as a mismatch.
- A cut-over without verification, or a rollback after old writes stopped.

### Today's build

| Piece | Job | Lesson section |
|---|---|---|
| `backfill` | copy one batch after the checkpoint, respecting versions; return the new checkpoint | the backfill |
| `verify` | mismatch rate and the mismatching keys | verification |
| `Migration` | `advance`, `rollback`, `read_from` | the six phases; the state machine |

Run: `uv run pytest weeks/w11-staff-judgment/d4-migrations -k "not review"`

---

## Day 5: Your stories, as data

Folder: `d5-star-bank`. Exercise: `w11d5_stars.py`.

### Why behavioral rounds decide the level

The coding and design rounds say whether to hire. The behavioral round and the project deep dive say at **which level**. Most strong engineers undersell themselves there, by telling **tasks** ("I built the evaluation pipeline") where the interviewer listens for **scope and judgment** ("three teams disagreed on what 'good' meant; I proposed a shared metric with data; two of them adopted it; regressions reaching production fell by half").

### STAR

A story has four parts:

| Part | Content | Share of the time |
|---|---|---|
| **S**ituation | the context, in two sentences | small |
| **T**ask | what had to be achieved, and why it was hard | small |
| **A**ction | what **you** did and decided: "I", not "we" | most of it |
| **R**esult | what changed, **with a number** | the end |

Plus two things that mark a senior story: the **signals** it demonstrates, and **what you would do differently**.

### Treat the stories like an evaluation set

- **A schema**: the same fields for every story.
- **Validation**: a result with no number is not a result; an action of one line is not an action; a story with no signal answers no question.
- **Coverage**: interviewers score along **axes**. Each axis needs at least two **valid** stories, so that a follow-up "give me another example" does not find you empty.
- **Retrieval**: given a question, pick the best story fast. A question asks for certain signals; the best story is the valid one that carries the most of them.

Axes used here, from public descriptions (loops change; confirm with your recruiter):

| Company | Axes |
|---|---|
| Meta | project impact, direction, engineering excellence, people |
| Google | general cognitive ability, role-related knowledge, leadership, "Googleyness" |
| across companies, at staff | scope, ambiguity, influence, technical depth, execution, people growth, conflict |

Only **valid** stories count toward coverage. A bank of twenty stories with no numbers covers nothing; counting them anyway hides the gaps the tool exists to show. That is today's review bug.

### After the tests pass: your real bank

Your stories are about your employer. They do not go into this public repo.

1. The format is in `private-template/stories.json`.
2. Your real file lives in a **separate private repository**.
3. `scripts/sync_private.sh` copies it into `reference/your-work/`, which git ignores.
4. Run `coverage` on it. The target: no gap at two stories per axis on the staff signals.

Nobody, and no AI, writes your stories. Write them, then ask for a critique against the axes.

### Traps of the day

- Invalid stories counted in the coverage.
- "We" throughout the action.
- A result such as "it went well".
- One favourite story used for every question.

### Today's build

| Function | Job | Lesson section |
|---|---|---|
| `validate_story` | the list of issues of one story | treat the stories like an evaluation set |
| `coverage` | per axis, the valid stories tagged with it | coverage |
| `gaps` | axes with too few stories | coverage |
| `pick_story` | the best valid story for the signals a question wants | retrieval |

Run: `uv run pytest weeks/w11-staff-judgment/d5-star-bank -k "not review"`

---

## End of the week

- **AI-off gate (15 min):** one drill from `drills/w11`, timer on, AI fully off: `uv run pytest drills/w11 -k d<number>`. Protocol: `drills/README.md`.
- **Reading slot (20 min, read only):** this week's file is row 11 of `reading/README.md`.
- **Ship one public thing** and log it in `SHIPLOG.md`: one claim, one piece of evidence. A write-up of this week's hardest lab with its numbers counts.
- **Tick `PROGRESS.md`**, write the retro, and name the hardest lab: next Monday you rewrite its main function from a blank file.

You are done with week 11 when you can do these without notes:

- [ ] bisect with a flaky check and say why one run is not evidence
- [ ] write the chain from symptom to "why it was not caught" for a real incident of yours
- [ ] state three properties of a function and explain shrinking
- [ ] recite the eight sections of a design document and say what non-goals are for
- [ ] recite the six phases of a migration, where rollback ends, and what a backfill must not overwrite
- [ ] tell one story in two minutes with "I", a number, and what you would change

## Optional depth (not needed for the labs)

- How each company and level is judged, with questions: `knowledge/12-staff-rubrics.md`
- The path beyond staff: `principal/README.md`
- Previous week: [`../w10-harness-serving/README.md`](../w10-harness-serving/README.md) · Next: [`../w12-mocks/README.md`](../w12-mocks/README.md)
