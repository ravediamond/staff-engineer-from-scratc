# Week 8: Reward models and preference learning

**Everything you need for this week is on this page.** You need week 7 (evaluation vocabulary, correlation). This week uses PyTorch on CPU; the section "PyTorch you need this week" covers all of it. Nothing from other folders is required.

A language model is trained to be useful by learning from human preferences: this answer was better than that one. The component that learns "better" is a reward model, and it is one of your specialties. This week you build the whole chain at toy size: from comparisons to scores, a trained reward model, its calibration and its biases, what goes wrong when you optimise against it, and the method that trains the policy directly from preferences.

## Start here

1. Read [The week in one table](#the-week-in-one-table) and [The ground for this week](#the-ground-for-this-week).
2. Each day, open that day's folder and follow [What to do each day](#what-to-do-each-day).
3. The lesson for each day is the matching section of this page: [Day 1](#day-1-bradleyterry-and-elo), [Day 2](#day-2-training-a-pairwise-reward-model), [Day 3](#day-3-calibration-and-length-bias), [Day 4](#day-4-best-of-n-and-over-optimisation), [Day 5](#day-5-dpo-process-rewards-then-a-design).
4. Friday: [End of the week](#end-of-the-week).

### What is in a day folder

| File | What it is | You |
|---|---|---|
| `predict.md` | small questions, answered before you read anything | write guesses |
| `README.md` | one-page summary of the day, with its "staff angle" | read after the lesson |
| `predict_run.py` | prints the real answers | run, compare |
| `w8dN_*.py` | **the exercise**, with `# TODO` | **write the code** |
| `test_w8dN_*.py` | tests | run, never edit |
| `review_w8dN.py` + its test | code with one planted bug | **find and fix**, write the `WHY:` line |
| `questions.md` | interview questions | answer out loud |

Friday's folder also has `design.md` (the prompt) and `rubric.md`. You write your answer in a new file, `my_design.md`.

### What to do each day

One hour, commands from the repo root.

| Min | Step | Command or file |
|---|---|---|
| 0–5 | Retrieve (Monday: 10-min delayed recall of last week's hardest function instead) | `uv run python scripts/review.py` |
| 5–10 | Guess, before reading | `predict.md` |
| 10–18 | Read the lesson | the day's section on this page |
| 18–20 | Check your guesses | `uv run python weeks/w8-reward-models/<day>/predict_run.py` |
| 20–45 | Build, narrating out loud | `uv run pytest weeks/w8-reward-models/<day> -k "not review"` until green |
| 45–53 | Review | `uv run pytest weeks/w8-reward-models/<day> -k review` |
| 53–60 | Explain | `questions.md` out loud, then `uv run python scripts/review.py add weeks/w8-reward-models/<day>` |

Guess before reading even if you know nothing: a wrong guess makes the lesson stick (`LEARNING.md` rule 1). AI stays off in the exercise files; stuck for 10 minutes, ask for a hint, not code.

## The week in one table

| Day | Folder | The question | You build | The review bug is about |
|---|---|---|---|---|
| Mon | `d1-bradley-terry` | how do comparisons become scores? | Bradley–Terry fitting; Elo | a sign |
| Tue | `d2-pairwise-rm` | how is a reward model trained? | a pairwise reward model with a leak-free split | how the data is split |
| Wed | `d3-rm-calibration` | are its probabilities honest? is it biased? | ECE, temperature scaling, a length-bias measure | a weighting |
| Thu | `d4-best-of-n` | what happens when you optimise against it? | best-of-N and the over-optimisation curve | which score is reported |
| Fri | `d5-dpo-process` | can the policy learn from preferences directly? | the DPO loss; step-level rewards; then a timed design | a missing term |

## The ground for this week

### Words

| Word | Meaning |
|---|---|
| policy `π` | the model that generates. `π(y \| x)` is the probability it gives to response `y` for prompt `x` |
| log-probability | `log π(y \| x)`: the usual way to handle these very small numbers |
| preference pair | `(prompt, chosen response, rejected response)`: a human judged one better |
| reward model (RM) | a network that gives a response a number, its **reward**, trained so that preferred responses score higher |
| RLHF | reinforcement learning from human feedback: train an RM on preferences, then train the policy to get high reward |
| proxy and gold | the proxy is what you can compute (the RM's score); the gold is what you actually want (true quality). They are never the same |
| `σ`, the sigmoid | `σ(z) = 1 / (1 + e^(−z))`: turns any number into a probability. `σ(0) = 0.5`; large positive → 1; large negative → 0 |
| `log σ(z)` | the log of that probability; the building block of every loss this week |

One number to remember: `−log σ(0) = log 2 ≈ 0.693`. It is the loss of a model that cannot tell two things apart, and the value to expect at step 0.

### PyTorch you need this week

```python
import torch
import torch.nn.functional as F

r = torch.zeros(3, requires_grad=True)             # three numbers to learn
opt = torch.optim.Adam([r], lr=0.1)                # the optimiser that will change them
for _ in range(100):
    loss = (r[0] - 1.0) ** 2 + (r[1] + 2.0) ** 2   # any formula built from r; smaller is better
    opt.zero_grad()                                # clear the previous gradients
    loss.backward()                                # compute how loss changes with each number
    opt.step()                                     # move the numbers a little to lower the loss
r.detach()                                         # about [1, -2, 0]: the values that minimise the loss
```

- A **tensor** is an array of numbers. `requires_grad=True` marks it as something to learn.
- **Training** is that loop: compute a loss, `backward()`, `step()`, repeat.
- `.detach()` returns the values without the machinery for learning; `with torch.no_grad():` computes without recording anything. Both are used for quantities that must **not** be learned.
- `F.logsigmoid(z)` computes `log σ(z)` safely for any `z`. Writing `torch.log(torch.sigmoid(z))` gives `−inf` for very negative `z`.
- A model is a class deriving from `torch.nn.Module`; `torch.nn.Linear(a, b)` is a layer from `a` numbers to `b` numbers; `torch.nn.ReLU()` between layers lets the network represent curves.

## Day 1: Bradley–Terry and Elo

Folder: `d1-bradley-terry`. Exercise: `w8d1_bt.py`.

### From comparisons to strengths

People are poor at giving absolute scores ("this answer is a 7") and decent at comparing ("this one is better"). The **Bradley–Terry model** turns a pile of comparisons into one number per item, its **strength** `r`:

```
P(i beats j) = σ( r_i − r_j )
```

Equal strengths give 0.5. A gap of 1 gives 0.73; a gap of 3 gives 0.95. Only **differences** matter: adding 10 to every strength changes nothing.

### Fitting

Find the strengths that make the observed outcomes most probable. For each comparison the model gave the winner a probability `σ(r_winner − r_loser)`. Multiply them all, take the log: the **log-likelihood**.

```
log-likelihood = Σ over comparisons of  log σ( r_winner − r_loser )
```

Maximise it, which in practice means minimise its negative with the loop above. Winner minus loser: the other way round, the fit ranks everything backwards. That is today's review bug.

Two details. Because only differences matter, the strengths can drift together; **centre** them at mean 0 at the end. And an item that never lost would get an infinite strength; a small penalty on `Σ r²` keeps the numbers finite.

**A reward model is Bradley–Terry** where the strength is no longer a free number per item, and is instead the output of a network that reads the prompt and the response. Same probability, same loss. That is tomorrow.

### Elo

The chess rating, also the first leaderboard of Chatbot Arena. It is the same model, updated one game at a time, with a different scale:

```
expected score of A:   E_a = 1 / ( 1 + 10^((R_b − R_a) / 400) )
after the game:        R_a ← R_a + K · ( S_a − E_a )          S_a = 1 win, 0.5 draw, 0 loss
```

A player who wins when expected to win gains little; an upset moves the ratings a lot. What A gains, B loses. Elo depends on the **order** of the games, so modern leaderboards fit Bradley–Terry on all comparisons at once.

### Traps of the day

- Loser minus winner.
- `log(sigmoid(…))` written by hand.
- Strengths not centred: two fits of the same data look different.
- An Elo update that is not zero-sum.

### Today's build

| Function | Job | Lesson section |
|---|---|---|
| `bt_prob` | probability that `i` beats `j` | from comparisons to strengths |
| `bt_log_likelihood` | sum of log-probabilities of the outcomes | fitting |
| `bt_fit` | fitted, centred strengths | fitting |
| `elo_expected`, `elo_update` | the two Elo formulas | Elo |

Run: `uv run pytest weeks/w8-reward-models/d1-bradley-terry -k "not review"`

---

## Day 2: Training a pairwise reward model

Folder: `d2-pairwise-rm`. Exercise: `w8d2_rm.py`.

### Data, model, loss

- **Data**: triples `(prompt, chosen, rejected)`.
- **Model**: `f(prompt, response) → one number`. Today an MLP (a few linear layers with ReLU between them) on a vector that stands for "prompt + response".
- **Loss**: Bradley–Terry with the network's outputs as strengths.

```
L = − mean log σ( f(x, chosen) − f(x, rejected) )
```

The model is never told what reward a response deserves, only which of two is better. The scale of the rewards is whatever the training finds.

### Two sanity checks

**Step 0.** An untrained network gives about the same reward to both responses, so the loss starts near `log 2 = 0.693`. Print it. A first loss of 5, or of 0.01, is a bug in the data or the loss before any learning.

**The metric is pairwise accuracy** on pairs the model never saw: the fraction where `f(chosen) > f(rejected)`. On real human data a good RM reaches 65 to 75%, not 95%, because humans disagree with each other. An accuracy that looks too good is a leak.

### Split by prompt, never by pair

Several pairs share one prompt. If pairs are split at random, the same prompt lands on both sides, the model learns features specific to that prompt, and the test accuracy is inflated: **leakage**. Choose the test **prompts** first (seeded shuffle of the distinct prompt ids), then send every pair to the side of its prompt, and check that the two sets of prompts do not intersect.

The same rule under other names: split by user, by document, by session. Whatever unit shares information must stay on one side.

### The training loop with batches

One pass over the data is an **epoch**. Each epoch: shuffle the indices, cut them into **minibatches**, and for each one run the three lines `zero_grad`, `backward`, `step`. **AdamW** is Adam with weight decay; it is the usual optimiser.

```python
g = torch.Generator().manual_seed(0)
perm = torch.randperm(10, generator=g)          # a seeded shuffle of 0..9
[perm[i:i + 4].tolist() for i in range(0, 10, 4)]      # three minibatches of indices
```

The network returns shape `(B, 1)` for a batch of `B`; the docstring wants `(B,)`. `.squeeze(-1)` removes the last axis. A loss between shapes `(B, 1)` and `(B,)` silently compares every item with every other.

### Traps of the day

- A split by pair.
- No step-0 loss printed.
- Accuracy measured on the training pairs.
- Output of shape `(B, 1)` left as it is.

### Today's build

| Piece | Job | Lesson section |
|---|---|---|
| `split_by_prompt` | train and test pairs with no shared prompt | split by prompt |
| `RewardModel` | MLP from a feature vector to one reward | data, model, loss |
| `pairwise_loss` | `−mean log σ(r_c − r_r)` | data, model, loss |
| `pair_accuracy` | fraction of pairs ordered correctly | two sanity checks |
| `train_rm` | AdamW, seeded minibatches, loss per epoch | the training loop |

Run: `uv run pytest weeks/w8-reward-models/d2-pairwise-rm -k "not review"`

---

## Day 3: Calibration and length bias

Folder: `d3-rm-calibration`. Exercise: `w8d3_calibration.py`.

### Is the probability honest?

For a pair, the RM gives a **margin** `m = r_chosen − r_rejected`, and `σ(m)` is its claimed probability that the first is preferred. A model is **calibrated** if its claims hold on average: among all the pairs where it says "80%", it is right about 80% of the time. Accuracy does not tell you this. A model can rank well and be wildly overconfident.

### Expected calibration error (ECE)

1. Cut [0, 1] into bins of equal width (say 10).
2. Put each prediction in the bin of its probability.
3. In each bin compare the mean predicted probability (**confidence**) with the fraction of positives actually observed (**accuracy**).
4. Average the gaps, **each bin weighted by its share of the samples**:

```
ECE = Σ over bins of  (n_bin / N) · | accuracy_bin − confidence_bin |
```

The weighting matters. A bin holding 2 samples out of 10 000 can have a gap of 0.5 by pure luck; unweighted, it counts as much as a bin holding half the data. That is today's review bug. Empty bins are skipped, and a probability of exactly 1.0 belongs to the last bin.

### Temperature scaling

The cheapest fix for overconfidence: divide every margin by one number `T` before the sigmoid.

```
calibrated probability = σ( m / T )
```

`T > 1` pulls probabilities toward 0.5 (less confident); `T < 1` pushes them apart. Dividing by a positive number never changes which response is preferred, so **accuracy is untouched**; only the confidence moves.

`T` is fitted on held-out pairs by minimising the **negative log-likelihood** (binary cross-entropy): the average of `−log` of the probability given to what actually happened. `T` must stay positive, so the number that is optimised is `log T`, and `T = exp(log T)`.

`F.binary_cross_entropy_with_logits(logits, labels)` computes that loss from margins directly.

### Length bias

Human raters tend to prefer longer answers, so an RM trained on their choices learns "longer is better". To measure it: take responses of **equal true quality** and compute the correlation between their reward and their length. It should be near 0. If it is clearly positive, the RM pays for length itself, and a policy optimised against it becomes verbose (tomorrow).

The comparison must be at equal quality. Over all responses, longer ones may really be better, and the correlation would prove nothing.

Mitigations: training pairs balanced in length; a length penalty; or length given to the model as an explicit input that is fixed at use time.

Pearson correlation of `x` and `y`: centre both, then `Σ(x·y) / sqrt( Σx² · Σy² )`.

### Traps of the day

- Unweighted ECE.
- Temperature fitted on the data used to report calibration.
- Optimising `T` directly and letting it go negative.
- Length bias measured on responses of mixed quality.

### Today's build

| Function | Job | Lesson section |
|---|---|---|
| `ece` | weighted calibration error | expected calibration error |
| `nll` | mean cross-entropy of `σ(m / T)` | temperature scaling |
| `fit_temperature` | the `T` that minimises it, through `log T` | temperature scaling |
| `pearson`, `length_bias` | correlation of reward with length | length bias |

Run: `uv run pytest weeks/w8-reward-models/d3-rm-calibration -k "not review"`

---

## Day 4: Best-of-N and over-optimisation

Folder: `d4-best-of-n`. Exercise: `w8d4_bon.py`.

### Best-of-N

The simplest way to use a reward model, with no training: sample `N` responses from the policy and return the one the RM scores highest. It works well, and it is a clean setting to see the central danger of the whole field.

How far has best-of-N moved from the original policy? There is an exact answer, as a KL divergence (a measure of distance between two distributions):

```
KL( best-of-N ‖ base ) = log N − (N − 1) / N
```

0 for `N = 1`, growing slowly: picking the best of 1 000 is "about 5.9 nats away" from the base policy.

### The over-optimisation curve

As `N` grows you push harder against the **proxy**, the RM. Two things happen:

- the **proxy** score of the selected sample keeps rising: by construction, you select for it;
- the **gold** score, the true quality, rises at first, reaches a peak, then **falls**.

The fall is the selection finding the RM's mistakes. Any proxy has regions where it is wrong; a strong enough search ends up exactly there. This is **Goodhart's law**: a measure that becomes a target stops being a good measure.

Today's toy world makes it visible. Each sample has a quality `q` and a length `l`. The proxy wrongly likes length; the gold penalises it. With small `N` the best-by-proxy sample is mostly a high-quality one. With large `N` it is the longest one in the batch.

Practical consequence: there is an optimal amount of optimisation, and it is found by measuring the **gold** as a function of the distance from the base policy, never by pushing the proxy as far as it goes.

### The cardinal rule

**Never report the quality of selected samples with the same RM that selected them.** That number is biased upward by construction: among `N` noisy scores, the highest is the one whose noise was most favourable (the winner's curse). Evaluate what was selected with something that took no part in the selection: a held-out judge, humans, or here the gold function. Reporting the proxy as if it were quality is today's review bug, and the most common over-claim in this area.

### Traps of the day

- The proxy score reported as quality.
- Selection by gold in the simulation: the curve then never falls and proves nothing.
- One random generator per `N` with the same seed: the curve's points are correlated in ways the docstring's single shared generator avoids.

### Today's build

| Function | Job | Lesson section |
|---|---|---|
| `bon_kl` | the closed form | best-of-N |
| `proxy`, `gold` | the two scores of the toy world | the over-optimisation curve |
| `best_of_n` | the highest-scoring sample, first on ties | best-of-N |
| `overoptimization_curve` | for each `N`: KL, mean proxy, mean gold of the picks | the over-optimisation curve |
| `gold_peak_n` | the `N` where gold is highest | the over-optimisation curve |

Run: `uv run pytest weeks/w8-reward-models/d4-best-of-n -k "not review"`

---

## Day 5: DPO, process rewards, then a design

Folder: `d5-dpo-process`. Exercise: `w8d5_dpo.py`. Also in the folder: `design.md`, `rubric.md`.

### DPO: no separate reward model

The classic pipeline has two stages: train an RM, then train the policy against it with reinforcement learning. **Direct preference optimisation (DPO)** does it in one, with a plain supervised loss on the policy.

The idea in three steps:

1. RLHF asks for a policy that gets high reward **while staying close to a reference policy** `π_ref` (the model before fine-tuning). "Close" is weighted by a constant `β`.
2. That problem has an exact solution, and the solution means that any policy `π` corresponds to an **implicit reward**: `r(x, y) = β · log( π(y | x) / π_ref(y | x) )`. A response the policy now favours more than the reference did is one with a high reward.
3. Put that reward into Bradley–Terry:

```
L_DPO = − mean log σ( β · [ (log π(y_c) − log π_ref(y_c)) − (log π(y_r) − log π_ref(y_r)) ] )
```

Minimising it raises the probability of the chosen response and lowers that of the rejected one, **relative to the reference**. The reference terms are what keep the policy from drifting anywhere: without them the loss rewards making `π(y_c)` large by any means, including forgetting everything else. Leaving them out is today's review bug.

**The step-0 check.** At the start the policy **is** the reference, the bracket is exactly 0, and the loss is `log 2`, whatever the log-probabilities are. A different first value means a missing or mis-signed term.

The reference is frozen: its log-probabilities are computed inside `torch.no_grad()`.

### Today's policy: a table

Each prompt has `K` candidate responses. The policy holds one learnable number (a **logit**) per prompt and per candidate, and turns each row into log-probabilities with a log-softmax:

```python
logits = torch.zeros(2, 4)                       # 2 prompts, 4 candidates, all equal
torch.log_softmax(logits, dim=-1)[0]             # four times log(1/4) = -1.386: a uniform policy
```

It is the smallest thing that has `log π(y | x)`, and enough to watch DPO move probability toward the chosen responses.

### Process rewards against outcome rewards

For a multi-step answer or an agent's trajectory, an **outcome** reward scores only the final result. A **process reward model (PRM)** scores each step. Step scores are combined into one:

| Aggregation | Meaning |
|---|---|
| **min** | a chain is as good as its worst step |
| **product** | if scores are probabilities, the probability that every step is right |
| **last** | only the final step |

The first step whose score falls below a threshold **locates** the error. That is the practical value: it says where a reasoning chain or an agent went wrong, for training (which step to blame) and for debugging.

### After the lab: the Friday design (45 minutes, timed)

`design.md`: reward model training and the preference data pipeline.

1. Start a 45-minute timer. Write in `my_design.md`, following the 45-minute frame of [week 5](../w5-design-method/README.md#the-45-minute-frame). Stop at the bell.
2. Grade yourself with `rubric.md`.
3. Only then read the model answer: `model_answer.md`, in the same folder on the `solutions` branch.
4. Write in `PROGRESS.md` the one thing that would have raised your level.

This week's deep dives: the split by prompt, rater disagreement, calibration, length bias, over-optimisation and how you would detect it.

### Traps of the day

- No reference terms.
- A gradient flowing into the reference.
- `β` outside the sigmoid.
- "Product" aggregation on scores that are not probabilities.

### Today's build

| Piece | Job | Lesson section |
|---|---|---|
| `dpo_loss` | the loss from four log-probabilities | DPO |
| `implicit_reward` | `β · (log π − log π_ref)` | DPO |
| `TablePolicy` | logits per prompt and candidate; `logp` | today's policy |
| `train_dpo` | full-batch Adam, frozen reference, loss history | DPO |
| `aggregate_prm`, `first_bad_step` | combine step scores; locate the first bad one | process rewards |

Run: `uv run pytest weeks/w8-reward-models/d5-dpo-process -k "not review"`

---

## End of the week

- **AI-off gate (15 min):** one drill from `drills/w08`, timer on, AI fully off: `uv run pytest drills/w08 -k d<number>`. Protocol: `drills/README.md`.
- **Reading slot (20 min, read only):** this week's file is row 8 of `reading/README.md`.
- **Ship one public thing** and log it in `SHIPLOG.md`: one claim, one piece of evidence. A write-up of this week's hardest lab with its numbers counts.
- **Tick `PROGRESS.md`**, write the retro, and name the hardest lab: next Monday you rewrite its main function from a blank file.

You are done with week 8 when you can do these without notes:

- [ ] write Bradley–Terry and its log-likelihood, and say why a reward model is the same thing
- [ ] write the pairwise loss, its step-0 value, and the right way to split the data
- [ ] define calibration and ECE; explain what temperature scaling changes and what it cannot
- [ ] explain length bias and how to measure it honestly
- [ ] draw the over-optimisation curve and state the cardinal rule
- [ ] write the DPO loss and say what the reference terms are for
- [ ] compare outcome and process rewards

## Optional depth (not needed for the labs)

- Interview questions with short answers: `knowledge/08-reward-models-and-preference-learning.md`
- Previous week: [`../w7-evaluation/README.md`](../w7-evaluation/README.md) · Next: [`../w9-distributed-training/README.md`](../w9-distributed-training/README.md)
