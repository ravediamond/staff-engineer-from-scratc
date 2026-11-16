# Week 7: Evaluation and experimentation

**Everything you need for this week is on this page.** You need week 6 day 3 (the bootstrap). The week is plain Python and the standard library. Nothing from other folders is required.

Evaluation is the specialty you already have. This week turns it into something you can write on a whiteboard and defend line by line: a harness as a measuring instrument, a calibrated LLM judge, the five statistical tools that cover most claims, online experiments and the ways they lie, and the link between offline numbers and what users do.

## Start here

1. Read [The week in one table](#the-week-in-one-table) and [The idea of the week](#the-idea-of-the-week).
2. Each day, open that day's folder and follow [What to do each day](#what-to-do-each-day).
3. The lesson for each day is the matching section of this page: [Day 1](#day-1-the-eval-harness), [Day 2](#day-2-calibrating-an-llm-judge), [Day 3](#day-3-statistics-for-evals), [Day 4](#day-4-online-ab-testing), [Day 5](#day-5-does-offline-predict-online).
4. Friday: [End of the week](#end-of-the-week).

### What is in a day folder

| File | What it is | You |
|---|---|---|
| `predict.md` | small questions, answered before you read anything | write guesses |
| `README.md` | one-page summary of the day, with its "staff angle" | read after the lesson |
| `predict_run.py` | prints the real answers | run, compare |
| `w7dN_*.py` | **the exercise**, with `# TODO` | **write the code** |
| `test_w7dN_*.py` | tests | run, never edit |
| `review_w7dN.py` + its test | code with one planted bug | **find and fix**, write the `WHY:` line |
| `questions.md` | interview questions | answer out loud |

Friday's folder also has `design.md` (the prompt) and `rubric.md`. You write your answer in a new file, `my_design.md`.

### What to do each day

One hour, commands from the repo root.

| Min | Step | Command or file |
|---|---|---|
| 0–5 | Retrieve (Monday: 10-min delayed recall of last week's hardest function instead) | `uv run python scripts/review.py` |
| 5–10 | Guess, before reading | `predict.md` |
| 10–18 | Read the lesson | the day's section on this page |
| 18–20 | Check your guesses | `uv run python weeks/w7-evaluation/<day>/predict_run.py` |
| 20–45 | Build, narrating out loud | `uv run pytest weeks/w7-evaluation/<day> -k "not review"` until green |
| 45–53 | Review | `uv run pytest weeks/w7-evaluation/<day> -k review` |
| 53–60 | Explain | `questions.md` out loud, then `uv run python scripts/review.py add weeks/w7-evaluation/<day>` |

Guess before reading even if you know nothing: a wrong guess makes the lesson stick (`LEARNING.md` rule 1). AI stays off in the exercise files; stuck for 10 minutes, ask for a hint, not code.

## The week in one table

| Day | Folder | The question | You build | The review bug is about |
|---|---|---|---|---|
| Mon | `d1-eval-harness` | is the new version better, or is it noise? | repeats, flakiness, slices, a paired bootstrap, a release gate | what is resampled |
| Tue | `d2-judge-calibration` | can I trust an LLM judge? | Cohen's κ, weighted κ, position consistency | chance agreement |
| Wed | `d3-eval-statistics` | which tool for which claim? | Wilson, McNemar, Holm, sample size, minimum detectable effect | which pairs count |
| Thu | `d4-online-ab` | what do real users do? | SRM check, z-test, CUPED, a peeking simulation | one term of a formula |
| Fri | `d5-offline-online` | does my offline metric predict anything? | rank correlations, sign agreement, a launch rule; then a timed design | how ties are ranked |

## The idea of the week

**An evaluation is a measuring instrument.** Like a scale or a thermometer it has a fixed input (the set of cases), **noise** (run it twice, get two numbers), a **resolution** (the smallest change it can detect), and it needs **calibration** against something trusted.

Most wrong claims in AI come from skipping one of these: a 2-point gain that is inside the noise, a judge nobody compared with humans, a test set too small to see the effect, twelve comparisons with one lucky winner.

Words used all week:

| Word | Meaning |
|---|---|
| case | one input with its expected output or its grading rule |
| confidence interval (CI) | a range that would contain the true value in 95% of repetitions of the experiment |
| p-value | the probability of a result at least this extreme if there were **no** real difference; below 0.05 by convention, chance is called unlikely |
| paired | both systems measured on the same cases |
| power | the probability of detecting a difference that really exists; usually set to 80% |
| `α` | the accepted probability of announcing a difference that does not exist; usually 5% |

## Day 1: The eval harness

Folder: `d1-eval-harness`. Exercise: `w7d1_harness.py`.

### Repeats and flakiness

A system with sampling, or with tools that sometimes fail, does not give the same output twice. Run every case several times. Report the mean **and** the spread per case. A case whose score varies across repeats beyond a tolerance is **flaky**: list it. Averaging it away hides that part of your result is luck.

```python
import statistics
statistics.pstdev([1.0, 1.0, 0.0]), statistics.pstdev([1.0, 1.0, 1.0])      # (0.471…, 0.0): the first case is flaky
```

`pstdev` is the population standard deviation: it divides by `n`.

### Slices

A **slice** is a subset of cases that share a property: a language, an intent, a customer, a difficulty. A global mean can stay flat while one slice collapses, when gains elsewhere hide the loss. Every regression that reaches production unnoticed was visible in a slice. Compute the mean per slice, always.

### Paired comparison

Two versions of the system, the same cases. Some cases are easy for both and some hard for both. That shared difficulty is by far the largest source of variation, and it says nothing about which version is better. Take the **difference per case** and it cancels.

**The paired bootstrap**: resample the **case ids** with replacement; for each resample compute the mean of `new − base` over the drawn cases; repeat. The 2.5th and 97.5th percentiles are a 95% interval for the improvement.

One draw of ids serves both systems. Drawing separately for each system destroys the pairing: the interval becomes several times wider, and real improvements look like noise. That is today's review bug.

### A release gate

A **gate** is a rule that decides "ship or not", **written before seeing the results** (pre-registered). Written after, a rule always finds a way to pass. Today's gate fails if any of these holds, and reports every reason:

- the whole interval of the improvement is below zero: a significant regression;
- the mean drops by more than a tolerance;
- any single slice drops by more than its tolerance.

### Traps of the day

- One run per case.
- The two systems resampled independently.
- A gate that stops at the first reason.
- Slices defined after looking at the results.

### Today's build

| Function | Job | Lesson section |
|---|---|---|
| `run_eval` | mean and spread per case over repeats | repeats and flakiness |
| `flaky` | cases whose spread exceeds a tolerance | repeats and flakiness |
| `slice_means` | mean per slice | slices |
| `paired_bootstrap` | improvement with its interval | paired comparison |
| `gate` | pass or fail, with reasons | a release gate |

Run: `uv run pytest weeks/w7-evaluation/d1-eval-harness -k "not review"`

---

## Day 2: Calibrating an LLM judge

Folder: `d2-judge-calibration`. Exercise: `w7d2_judge.py`.

### A judge is an instrument with unknown bias

Using a model to grade outputs is cheap and scales. Until it has been compared with human labels on the same items, nobody knows what it measures. Three checks before trusting one.

### Check 1: agreement beyond chance (Cohen's κ)

Raw agreement misleads. If 90% of the answers are good, a judge that says "good" every time agrees with the humans 90% of the time and has measured nothing.

```
p_o = fraction of items where judge and human agree
p_e = Σ over labels of  P(judge says the label) × P(human says the label)        agreement expected by chance
κ   = (p_o − p_e) / (1 − p_e)
```

κ is 1 for perfect agreement and 0 for what chance alone would give. In the example: `p_e = 1.0 × 0.9 + 0 × 0.1 = 0.9`, `p_o = 0.9`, κ = 0.

`p_e` uses the label frequencies of **both** raters, one factor from each. Computing it from one rater's frequencies alone is today's review bug.

Rough reading: below 0.4 poor; 0.4 to 0.6 moderate; 0.6 to 0.8 substantial; above 0.8 near perfect. Below 0.6, fix the judge's instructions before using its numbers.

A **confusion matrix** holds the counts: row `i`, column `j` = the number of items the first rater labelled `i` and the second labelled `j`. The diagonal is agreement.

### Check 2: scales with an order (weighted κ)

On a 1-to-5 scale, a judge that says 4 where the human said 5 is nearly right; one that says 1 is badly wrong. Plain κ counts both as "disagree". **Weighted κ** charges each disagreement by its distance. With quadratic weights:

```
w_ij = (i − j)² / (k − 1)²                   0 on the diagonal, 1 for the two extremes
κ_w  = 1 − Σ w · observed / Σ w · expected          expected = product of the two raters' frequencies
```

### Check 3: position bias

A judge that compares two answers often prefers the one shown first. Ask each pair twice, as (A, B) and as (B, A). A consistent judge names the same **answer** both times. The **consistency rate** is the fraction of pairs where it does. A simple correction: keep a verdict only when both orders agree, and call the rest a tie.

Two other known biases: longer answers win (verbosity), and a model prefers outputs of its own family (self-preference).

### Traps of the day

- Raw agreement reported as quality.
- Chance agreement from one rater's frequencies.
- Verdicts of the swapped order not mapped back to the same answers before comparing.
- A κ of 0.3 noted and the judge used anyway.

### Today's build

| Function | Job | Lesson section |
|---|---|---|
| `confusion` | the matrix of counts | check 1 |
| `cohen_kappa` | chance-corrected agreement | check 1 |
| `weighted_kappa` | quadratic weights over ordered labels | check 2 |
| `position_consistency` | rate of consistent verdicts | check 3 |
| `debiased_verdicts` | the verdict if both orders agree, else a tie | check 3 |

Run: `uv run pytest weeks/w7-evaluation/d2-judge-calibration -k "not review"`

---

## Day 3: Statistics for evals

Folder: `d3-eval-statistics`. Exercise: `w7d3_stats.py`.

Five tools cover most claims. `statistics.NormalDist` from the standard library gives the `z` values:

```python
import statistics
statistics.NormalDist().inv_cdf(0.975), statistics.NormalDist().inv_cdf(0.80)      # 1.96 (two-sided 5%), 0.84 (80% power)
```

### Tool 1: the Wilson interval, for a pass rate

`k` passes out of `n`, `p = k/n`, `z = 1.96`:

```
centre     = ( p + z²/(2n) ) / ( 1 + z²/n )
half-width = z · sqrt( p(1−p)/n + z²/(4n²) ) / ( 1 + z²/n )
```

7 out of 10 gives (0.40, 0.89). Use it in place of the textbook `p ± 1.96 · sqrt(p(1−p)/n)`, which breaks at small `n` and near 0 or 1: for 10 out of 10 it returns the interval (1, 1).

### Tool 2: McNemar's test, for two systems on the same cases

Sort the cases in four groups: both pass, both fail, only A passes (`b` cases), only B passes (`c` cases). Cases where the two agree say nothing about which is better. Only the `b + c` **discordant** cases count.

If the systems were equally good, each discordant case would be a fair coin between "only A" and "only B". The p-value is the probability, under that coin, of a split at least as uneven as the one observed:

```
p = min( 1,  2 · P( Binomial(b + c, 0.5) ≤ min(b, c) ) )        P(X ≤ j) = Σ_{i=0..j} C(b+c, i) / 2^(b+c)
```

`math.comb(n, i)` gives the binomial coefficient. Using all the cases in place of the discordant ones is today's review bug.

### Tool 3: Holm's correction, for many comparisons

Test 12 slices at 5% each and the chance of at least one false alarm is `1 − 0.95¹² = 46%`. **Holm's procedure** keeps the chance of any false alarm at 5%:

1. Sort the `m` p-values, smallest first.
2. Compare the smallest with `α/m`, the next with `α/(m−1)`, and so on.
3. Reject while the p-value is at or below its threshold; **stop at the first one that is not**, and reject nothing after it.

The result must be returned in the original order of the inputs.

### Tool 4: sample size

How many cases per system to tell a pass rate `p1` from `p2`, with `α = 5%` and 80% power?

```
p̄ = (p1 + p2)/2
n = ( z_{α/2} · sqrt(2 p̄ (1 − p̄)) + z_β · sqrt( p1(1−p1) + p2(1−p2) ) )² / (p1 − p2)²        rounded up
```

The difference is squared in the denominator: telling 70% from 75% needs about 1 250 cases per system; 70% from 80%, about 290.

### Tool 5: minimum detectable effect

The same formula read backwards: with my `n` cases, what is the smallest difference I could detect? Search for the smallest `d` such that `n_per_arm(p, p + d) ≤ n`. With 200 cases around 70% it is about 12 points. **Say this number before showing any result**: a set that cannot see a 5-point change cannot show that there is no 5-point regression.

### Traps of the day

- The simple interval at `n = 20`.
- McNemar on all cases.
- Holm continuing after the first failure.
- A sample size rounded down.

### Today's build

| Function | Job | Lesson section |
|---|---|---|
| `wilson` | interval for a rate | tool 1 |
| `mcnemar_exact` | two-sided exact p-value from the discordant counts | tool 2 |
| `holm` | which hypotheses are rejected | tool 3 |
| `n_per_arm` | cases needed per system | tool 4 |
| `mde` | smallest detectable difference | tool 5 |

Run: `uv run pytest weeks/w7-evaluation/d3-eval-statistics -k "not review"`

---

## Day 4: Online A/B testing

Folder: `d4-online-ab`. Exercise: `w7d4_ab.py`.

### Why online

Offline evaluations approximate users. An **A/B test** measures them: users are split at random between the current version (A, control) and the new one (B, treatment), and a metric such as the conversion rate is compared. Four things go wrong.

### 1. Sample ratio mismatch (SRM)

You asked for a 50/50 split and observe 50 912 users against 49 088. Chance, or a bug? A chi-square test compares the observed counts with the expected ones:

```
χ² = Σ over the two groups of (observed − expected)² / expected          p = erfc( sqrt(χ² / 2) )
```

```python
import math
exp = (50912 + 49088) / 2
chi2 = (50912 - exp) ** 2 / exp + (49088 - exp) ** 2 / exp
math.erfc(math.sqrt(chi2 / 2))               # about 8e-9: this split is not chance
```

If `p < 0.001`, **stop**. The assignment or the logging is broken: some users are missing from one group, and they are not a random sample. Every metric of the experiment is suspect. Check SRM before reading anything else.

### 2. The test: two proportions

```
p̂ = (conversions_A + conversions_B) / (n_A + n_B)             the pooled rate
z = (p_B − p_A) / sqrt( p̂ (1 − p̂) (1/n_A + 1/n_B) )
```

`z` says how many standard errors apart the two rates are. Beyond ±1.96 the two-sided p-value is below 0.05. The denominator needs **both** `1/n` terms.

### 3. Variance reduction: CUPED

Users differ a lot from each other, and that spread hides small effects. For each user you usually know a value from **before** the experiment, such as last month's activity. It predicts part of their behaviour during the experiment, and that part has nothing to do with the treatment. **CUPED** subtracts it:

```
θ = cov(x, y) / var(x)                  x: the pre-experiment value, y: the metric
y' = y − θ · (x − mean(x))
```

The mean of `y'` equals the mean of `y`; its variance is multiplied by `1 − ρ²`, where `ρ` is the correlation between `x` and `y`. With `ρ = 0.7` the variance halves: the same power with half the users.

### 4. Peeking

You look at the p-value every day and stop the first time it is below 0.05. Each look is another chance to cross the line by luck. With 10 looks the false-positive rate is not 5%; it is several times that. Today you simulate it with an **A/A test** (both groups get the same version, so any "significant" result is false by construction) and count how often it stops.

Fixes: decide the duration in advance and look once; or use a stricter threshold at each look. The simplest is `α / number of looks`; real platforms use sequential tests that waste less.

### Traps of the day

- Reading the metric before the SRM check.
- A z-test without the pooled rate, or with one `1/n` term.
- CUPED with a covariate measured **during** the experiment: it can absorb the treatment effect itself.
- Stopping at the first significant day.

### Today's build

| Function | Job | Lesson section |
|---|---|---|
| `srm_pvalue` | is the split what was asked? | SRM |
| `two_prop_z` | `z` and the two-sided p-value | the test |
| `cuped`, `variance_reduction` | adjusted metric, `θ`, and the gain | CUPED |
| `peeking_false_positive_rate` | simulate A/A tests with repeated looks | peeking |

Run: `uv run pytest weeks/w7-evaluation/d4-online-ab -k "not review"`

---

## Day 5: Does offline predict online?

Folder: `d5-offline-online`. Exercise: `w7d5_offline_online.py`. Also in the folder: `design.md`, `rubric.md`.

### The question

An offline metric is worth what it predicts about users. If a gain on your test set does not usually become a gain in the A/B test, the offline metric is decoration. You can measure this directly, with the history of past launches: for each one, an offline score and an online result.

### Rank correlation

Do the two measures **order** the model versions the same way?

**Kendall's τ** looks at every pair of versions. A pair is **concordant** if both measures rank the two versions in the same order, **discordant** if in opposite orders.

```
τ = (concordant − discordant) / (number of pairs)             number of pairs = n(n−1)/2
```

1 is the same order, −1 the opposite, 0 no relation. A pair tied on either measure counts as neither.

**Spearman's ρ** replaces each value by its **rank** and takes the ordinary correlation of the ranks. Tied values share the **average** of the ranks they occupy: values `[10, 20, 20, 30]` get ranks `[1, 2.5, 2.5, 4]`. Giving ties the ranks 2 and 3 in the order they happen to appear makes the result depend on the order of the rows. That is today's review bug.

Pearson correlation of `a` and `b`: centre both, then `Σ(a·b) / sqrt( Σa² · Σb² )`.

### Sign agreement

The plainest number: over past launches, how often did the offline change and the online change have the same sign? At 60%, the offline evaluation is barely better than a coin. Launches with a change of exactly zero on either side are left out.

### A launch rule, as code

Written before the experiment, so that nobody argues afterwards. The inputs are the interval of the offline improvement, the interval of the online improvement, and the list of **guardrail** breaches. A guardrail is a metric that must not get worse (latency, cost, safety), whatever happens to the main one. The rules are applied in a fixed order and the first that matches decides: ship, iterate or roll back. The docstring gives the order.

### After the lab: the Friday design (45 minutes, timed)

`design.md`: evaluation infrastructure for an AI product with 30 teams.

1. Start a 45-minute timer. Write in `my_design.md`, following the 45-minute frame of [week 5](../w5-design-method/README.md#the-45-minute-frame). Stop at the bell.
2. Grade yourself with `rubric.md`.
3. Only then read the model answer: `model_answer.md`, in the same folder on the `solutions` branch.
4. Write in `PROGRESS.md` the one thing that would have raised your level.

### Traps of the day

- Ties ranked by position.
- Tied pairs counted as concordant.
- Zero deltas counted as agreement.
- A launch rule that checks the main metric before the guardrails.

### Today's build

| Function | Job | Lesson section |
|---|---|---|
| `kendall_tau` | concordant minus discordant pairs | rank correlation |
| `average_ranks`, `spearman` | ranks with ties, then correlation | rank correlation |
| `sign_agreement` | share of launches where the two signs match | sign agreement |
| `launch_decision` | ship, iterate or roll back | a launch rule |

Run: `uv run pytest weeks/w7-evaluation/d5-offline-online -k "not review"`

---

## End of the week

- **AI-off gate (15 min):** one drill from `drills/w07`, timer on, AI fully off: `uv run pytest drills/w07 -k d<number>`. Protocol: `drills/README.md`.
- **Reading slot (20 min, read only):** this week's file is row 7 of `reading/README.md`.
- **Ship one public thing** and log it in `SHIPLOG.md`: one claim, one piece of evidence. A write-up of this week's hardest lab with its numbers counts.
- **Tick `PROGRESS.md`**, write the retro, and name the hardest lab: next Monday you rewrite its main function from a blank file.

You are done with week 7 when you can do these without notes:

- [ ] describe an evaluation as an instrument: input, noise, resolution, calibration
- [ ] explain the paired bootstrap and why both systems share one resample
- [ ] compute Cohen's κ by hand on a small table and say what position bias is
- [ ] write the Wilson interval; explain McNemar with the discordant pairs; apply Holm
- [ ] say what your test set can and cannot detect
- [ ] name the four ways an A/B test goes wrong and the fix for each
- [ ] say how you would check that an offline metric predicts online results

## Optional depth (not needed for the labs)

- Interview questions with short answers: `knowledge/07-evaluation-and-experimentation.md`
- Previous week: [`../w6-rag/README.md`](../w6-rag/README.md) · Next: [`../w8-reward-models/README.md`](../w8-reward-models/README.md)
