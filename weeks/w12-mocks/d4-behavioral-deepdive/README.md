# W12 D4: behavioral + project deep dive (2 × 45 minutes)

## Part 1: behavioral (45 min)
Have someone read `script.md` to you (or record the questions and play them back). 6 questions,
~6 minutes each including follow-ups. Answer from your STAR bank (W11 D5), out loud, recorded.

## Part 2: project deep dive (45 min)
Pick your strongest project (a `case-file.md` in your private repo). The interviewer goes **deep**: architecture,
the numbers, the alternatives, what broke, what you personally did. The deep-dive question list is in
`script.md`. The interviewer's goal is to find the edge of your knowledge; yours is to show where it is honestly.

## Scoring
Score each answer with the rubric in `script.md`, then compute the decision with `w12d4_scorer.py`
(the build for today): weighted axes, per-axis floors, and a hire/lean/no decision, the same way calibrated
loops aggregate interviewer scores.

## Today's build (`w12d4_scorer.py`)

`normalize(weights)`, `weighted_score(scores, weights)`, `decision(scores, weights, floors, bar)` → `"strong hire" | "hire" | "lean no" | "no hire"`.
