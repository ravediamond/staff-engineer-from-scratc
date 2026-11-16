# Week 12: Mocks

**Everything you need for this week is on this page.** This week teaches nothing new: it tests weeks 1 to 11 in the formats of a real loop. Each day's section says how to run the round, what is scored, and where on the earlier week pages to repair what failed.

Five full rounds under real conditions: timer, blank file, talking out loud, recorded. Each day ends with a score, the level it signals, and the single biggest gap. If you can, do at least two of them with a human (a friend at a large company, a paid mock platform, a former colleague): grading yourself is useful, an outside interviewer is better.

## Start here

1. Read [The week in one table](#the-week-in-one-table) and [Rules for every mock day](#rules-for-every-mock-day).
2. Each day, read that day's section here first, then open the folder: [Day 1](#day-1-coding-mock-a), [Day 2](#day-2-coding-mock-b), [Day 3](#day-3-design-mocks), [Day 4](#day-4-behavioral-and-project-deep-dive), [Day 5](#day-5-take-home-pair-programming-final-retro).
3. Friday: [End of the week](#end-of-the-week).

## The week in one table

| Day | Folder | The round | Format | You write |
|---|---|---|---|---|
| Mon | `d1-coding-a` | coding | 2 problems, 35 minutes, blank functions | `w12d1_mock.py`, then the review file |
| Tue | `d2-coding-b` | coding | 2 problems, 35 minutes; then review a candidate's solution | `w12d2_mock.py`, then the review file |
| Wed | `d3-design-mocks` | system design + ML design | two written designs of 45 minutes, with a 15-minute break | two design files, then a small capacity build |
| Thu | `d4-behavioral-deepdive` | behavioral + project deep dive | 45 minutes each, questions read to you, recorded | spoken answers, then a scorer |
| Fri | `d5-takehome-pairing` | take-home + pair programming | a 4-hour take-home (weekend); a 45-minute pairing session; the final retro | a small repo; two features in existing code |

## Rules for every mock day

1. **Timer visible. Stop at the bell,** even in the middle of a line. In the room nobody gives you five more minutes.
2. **No notes, no documentation, no autocomplete, AI fully off.**
3. **Do not open the build file before the timer starts.** The problem statement is in the day's `README.md`; reading it is the first minute of the round.
4. **Talk out loud and record the audio.** The same day, listen to five minutes of it and count three things: filler words, silences longer than 20 seconds, and claims you did not verify.
5. **Grade with the rubric before reading any model answer.**
6. **Write the biggest gap in `PROGRESS.md`.** Next week's practice targets it.

This page gives the method for each round. It deliberately says nothing about how to solve the problems.

Start each day with the spaced retrieval as usual: `uv run python scripts/review.py`.

## Day 1: Coding mock A

Folder: `d1-coding-a`. Exercise: `w12d1_mock.py`. Also in the folder: `rubric.md`.

### The round

Two problems, 35 minutes in total: about 15 for the first and 20 for the second. The statements are in the day's `README.md`. The functions in the build file are blank.

```
uv run pytest weeks/w12-mocks/d1-coding-a -k "not review"       # only after the timer
uv run pytest weeks/w12-mocks/d1-coding-a -k review             # then: review a candidate's solution
```

The review file is a solution that passed its author's own examples. Find what is wrong with it, fix it, write the `WHY:` line. Then score yourself with `rubric.md`.

### How to spend 15 minutes on one problem

| Minutes | What you do | What the interviewer scores |
|---|---|---|
| 0–2 | restate the problem; one worked example; the edge cases | did you understand before typing? |
| 2–4 | brute force and its cost; the better idea and its cost; **wait for a nod** | can you compare approaches? |
| 4–5 | the invariant, in one sentence | do you know why it is correct? |
| 5–12 | code, narrating intent | is it clean? can I follow you? |
| 12–15 | walk one example through the code by hand; then the edge cases | do you verify your own work? |

This is the five-step protocol of [week 1, day 1](../w1-coding-base/README.md#day-1-binary-heap-heapify-top-k). The most common way to lose a round you could have passed: typing in silence for ten minutes, then discovering a misunderstanding.

If you are stuck: say what you know, propose the brute force, and start from it. A working slow solution with a clear path to the fast one scores above an unfinished clever one.

### After the round: where to repair

Find the pattern each problem needed in `drills/PATTERNS.md`, then re-read the matching lesson: [week 1](../w1-coding-base/README.md) for the core structures, [week 2](../w2-reliability/README.md) for limits and scheduling under constraints. Redo the problem tomorrow from a blank file.

## Day 2: Coding mock B

Folder: `d2-coding-b`. Exercise: `w12d2_mock.py`. Also in the folder: `rubric.md`.

### The round

Same format: two problems, 35 minutes, statements in the day's `README.md`.

```
uv run pytest weeks/w12-mocks/d2-coding-b -k "not review"
uv run pytest weeks/w12-mocks/d2-coding-b -k review
```

### Reviewing someone else's code

The second half of today is a skill of its own, and at staff level it is scored: you review more code than you write. A method:

1. **Read the contract first**: the docstring, the guarantees it claims.
2. **State the invariant** the code must keep, before reading the body.
3. **Read the body against the invariant**, line by line. Where does it stop holding?
4. **Hunt at the edges**: empty input, one element, all equal, the capacity limit, the first and last iteration of each loop.
5. **Construct the smallest input that breaks it**, and run it. A review comment with a failing input ends the discussion.
6. **Say what is good** too, and separate "wrong" from "I would write it differently".

### After the round: where to repair

`drills/PATTERNS.md` for the patterns; [week 1](../w1-coding-base/README.md) and the drills of weeks 3 to 5 for graph search and counting under memory limits. Redo from blank tomorrow.

## Day 3: Design mocks

Folder: `d3-design-mocks`. Exercise: `w12d3_capacity.py`. Also in the folder: `ml_design.md`, `rubric.md`, `system_design.md`.

### The round

Two full designs back to back, with a 15-minute break, as in a real loop:

1. `system_design.md`: a general system design round.
2. `ml_design.md`: an ML system design round.

For each: a 45-minute timer, your answer in a new file (`my_system_design.md`, `my_ml_design.md`), then grade with `rubric.md`, and only then read the model answers on the `solutions` branch (`model_answer_system.md`, `model_answer_ml.md`).

Use the 45-minute frame of [week 5](../w5-design-method/README.md#the-45-minute-frame) exactly: requirements with numbers and non-goals, estimation, API and data, the simple design, two deep dives you choose, wrap-up.

### What an ML design round adds

The frame is the same. The content of each phase changes:

| Phase | In an ML design round |
|---|---|
| requirements | the **metric** that defines success, and the cost of each kind of error (a false positive and a false negative rarely cost the same) |
| estimation | examples per day, labels available, tokens and GPUs, cost per prediction |
| data | where labels come from, how fresh, how biased; the train/test split and what must not leak (week 8) |
| design | the **simplest baseline first** (rules, a small model), then what a larger model buys |
| deep dives | **evaluation** offline and online (week 7), failure modes, human fallback, monitoring for drift |
| wrap-up | how you would know in a month that it is working; what you would not build yet |

Two sentences that mark the level: "the baseline I would ship first is…", and "I would know it is wrong when…".

### The build

`w12d3_capacity.py` is small on purpose: it computes the capacity numbers the two prompts need, so that you can check the arithmetic you did in your head during the round. Do it **after** both designs.

```
uv run pytest weeks/w12-mocks/d3-design-mocks -k "not review"
```

### After the round: where to repair

Estimation: [week 5, day 1](../w5-design-method/README.md#day-1-back-of-the-envelope-estimation). Storage and retrieval choices: [week 4](../w4-storage-retrieval/README.md). Evaluation and launch rules: [week 7](../w7-evaluation/README.md). Serving cost: [week 10, day 4](../w10-harness-serving/README.md#day-4-serving-arithmetic).

## Day 4: Behavioral and project deep dive

Folder: `d4-behavioral-deepdive`. Exercise: `w12d4_scorer.py`. Also in the folder: `script.md`.

### Part 1: behavioral (45 minutes)

Have someone read `script.md` to you, or record the questions and play them back. Six questions, about six minutes each with follow-ups. Answer out loud from your story bank ([week 11, day 5](../w11-staff-judgment/README.md#day-5-your-stories-as-data)), recorded.

For each answer: situation and task in under 30 seconds; most of the time on what **you** decided and did; a result with a number; what you would change. When the follow-up comes ("why not the other option?", "who disagreed?"), answer it directly. The follow-ups are where the level is read.

### Part 2: project deep dive (45 minutes)

Pick your strongest project: one `case-file.md` in your private repo (format in `private-template/case-file.md`). The interviewer goes **deep**: the architecture, the numbers, the alternatives you rejected, what broke, what you personally did. The question list is in `script.md`.

The interviewer's goal is to find the edge of your knowledge. Yours is to show honestly where it is. "I don't know; here is how I would find out" is a strong answer. A confident guess that turns out wrong ends the round.

Every number you say must be one you can re-derive (format in `private-template/numbers.md`). If you cannot re-derive it from raw data with your own code, you do not say it.

### Scoring, and the build

Score each answer with the rubric in `script.md`. Then `w12d4_scorer.py` turns the scores into a decision the way calibrated loops do: a weight per axis, a **floor** per axis, and a bar.

The floor is the part people forget: one axis clearly below the bar is not compensated by excellence elsewhere. A brilliant design round does not rescue a behavioral round that showed no ownership.

```
uv run pytest weeks/w12-mocks/d4-behavioral-deepdive -k "not review"
```

### After the round: where to repair

Stories with no number, or told with "we": [week 11, day 5](../w11-staff-judgment/README.md#day-5-your-stories-as-data). A project you could not defend in depth: write its case file, with the chain of [week 11, day 1](../w11-staff-judgment/README.md#day-1-root-cause) for what broke and the alternatives section of [day 3](../w11-staff-judgment/README.md#day-3-design-documents).

## Day 5: Take-home, pair programming, final retro

Folder: `d5-takehome-pairing`. Exercise: `w12d5_pairing.py`. Also in the folder: `takehome.md`.

Paris unicorns often use a take-home or a pairing session on a realistic codebase in place of, or on top of, algorithm rounds.

### Part 1: the take-home (4 hours, on a weekend day)

The specification is in `takehome.md`. Timebox it strictly. Submit to yourself as you would to a company: a repository, a README, tests.

What reviewers look at, in order: does it run from the README in one command; are there tests, and do they test behaviour; is the scope what was asked, no more; does the README state the trade-offs and what you would do with more time. A small, finished, tested solution beats a large unfinished one every time.

### Part 2: pair programming (45 minutes)

`w12d5_pairing.py` is an existing small evaluation runner, already used by a team. Your pair asks for two features (they are described in the day's `README.md`).

How to run the session:

1. **Read the existing code first** (5 minutes). Say out loud what each function does.
2. **Ask questions before changing anything**: what must keep working? what is the expected behaviour in the unclear case?
3. **Small steps, with the tests**: one change, run, next.
4. **Keep the old behaviour** where the request does not ask to change it.
5. Narrate.

```
uv run pytest weeks/w12-mocks/d5-takehome-pairing -k "not review"
uv run pytest weeks/w12-mocks/d5-takehome-pairing -k review        # last 5 minutes: review a teammate's change
```

### Part 3: the final retro (30 minutes)

Fill the last section of `PROGRESS.md`: for each kind of round, your score this week against your first attempt; the three biggest gaps left; the plan for the next four weeks (keep drilling the weakest round, keep the ship log weekly); and the date you will apply to your first three companies.

## End of the week

- **AI-off gate (15 min):** one drill from `drills/w12`, timer on, AI fully off: `uv run pytest drills/w12 -k d<number>`. Protocol: `drills/README.md`.
- **Reading slot (20 min, read only):** this week's file is row 12 of `reading/README.md`.
- **Ship one public thing** and log it in `SHIPLOG.md`: one claim, one piece of evidence. A write-up of this week's hardest lab with its numbers counts.
- **Tick `PROGRESS.md`**, write the retro, and name the hardest lab: next Monday you rewrite its main function from a blank file.

- **Keep the cards alive:** `uv run python scripts/review.py` daily. The long intervals are where retention is built.
- **Ship one public thing** and log it in `SHIPLOG.md`.
- **Check for blind spots:** `SELF_AUDIT.md`, each line out loud in two minutes.

You are ready for a loop when you can:

- [ ] solve two medium problems in 35 minutes while narrating, and test them by hand
- [ ] find the bug in someone else's passing solution and show the input that breaks it
- [ ] run a 45-minute design with numbers, non-goals and two deep dives of your choosing
- [ ] answer six behavioral questions with "I", a number, and a lesson
- [ ] defend your strongest project to the edge of your knowledge, and say where the edge is
- [ ] deliver a small, tested take-home on time

## What comes next

Part 2, from week 13 (`ROADMAP.md`): streaming, Kubernetes, databases. The two topics you said went badly in past interviews are weeks 13 and 14, each with a hands-on track on real tools in `handson/`.

## Optional depth (not needed for the rounds)

- A mixed bank of questions for warm-up: `knowledge/13-question-bank.md`
- How each company and level is judged: `knowledge/12-staff-rubrics.md`
- Previous week: [`../w11-staff-judgment/README.md`](../w11-staff-judgment/README.md) · Next: [`../w13-streaming/README.md`](../w13-streaming/README.md)
