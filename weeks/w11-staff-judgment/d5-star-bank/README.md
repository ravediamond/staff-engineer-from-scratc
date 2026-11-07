# W11 D5: your STAR bank as data, scored against level rubrics

Primer: `knowledge/12-staff-rubrics.md` §1–2 (Meta, Google, Paris unicorns).

## The one idea

Behavioral rounds decide the level. Most strong engineers fail them by telling **tasks** ("I built X")
instead of **scope and judgment** ("three teams disagreed; I proposed Y with data; Z changed"). Treat your
stories like an eval set:

- A **schema** (situation, task, action, result, numbers, signals, what I would change).
- **Validation**: results need a number; actions need substance; every story needs signals.
- **Coverage**: every axis interviewers score must have at least two strong stories.
- **Retrieval**: given a question's signals, pick the best story fast.

Axes used here (public descriptions; loops evolve, check with your recruiter):
- **Meta** (performance axes used in behavioral calibration): project impact, direction, engineering excellence, people.
- **Google** (hiring attributes): general cognitive ability, role-related knowledge, leadership, "Googleyness".
- **Staff signals** (cross-company): scope, ambiguity, influence, technical depth, execution, people growth, conflict.

## Today's build (`w11d5_stars.py`)

`validate_story(s)` → issues, `coverage(stories, axes)` → `{axis: [ids]}` (only valid stories count),
`gaps(cov, min_stories)`, `pick_story(stories, wanted_signals)`.

Then fill `stories.json` in your **private** repo (format: `private-template/stories.json`), sync it,
and run `coverage` on it. Target: zero gaps at `min_stories=2` on the staff signals.

## Staff angle

The best behavioral answers are the same as the best design docs: context with a number, options,
a decision, a measured outcome, and what you learned. If your story bank is weak on "influence" or
"conflict", that is not an interview problem; it is a signal about which work to seek next quarter.
