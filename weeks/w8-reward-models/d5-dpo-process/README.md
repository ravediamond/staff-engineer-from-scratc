# W8 D5: DPO from scratch, process vs outcome rewards + Friday design

Primer: `knowledge/08-reward-models-and-preference-learning.md` §5–6.
Reference: Rafailov et al., "Direct Preference Optimization" (2023); Lightman et al., "Let's Verify Step by Step" (2023).

## The one idea

**DPO** skips the explicit reward model. The KL-regularised RL objective has a closed-form optimal
policy, which implies an **implicit reward** `r(x, y) = β · log(π_θ(y|x) / π_ref(y|x))`. Plug it
into Bradley–Terry and you get a loss on the policy directly:

```
L_DPO = −mean log σ( β · [ (log π_θ(y_c) − log π_ref(y_c)) − (log π_θ(y_r) − log π_ref(y_r)) ] )
```

When `π_θ == π_ref` the bracket is 0 and the loss is `log 2`, whatever the log-probabilities. That
is the step-0 sanity check, and the test that catches a missing reference term.

Today's "policy" is a table of logits: each prompt has K candidate responses, so `log π(y|x)` is a
log-softmax over K. Enough to watch DPO move probability mass to chosen responses.

**Process vs outcome rewards** for multi-step reasoning or agent trajectories: an outcome RM scores
the final answer; a process RM (PRM) scores each step. Aggregations: **min** (a chain is as good as
its worst step), **product** (probability all steps are right), **last**. The first step below a
threshold localises the error (useful for credit assignment and for debugging agents).

## Today's build (`w8d5_dpo.py`)

`dpo_loss(pc, pr, rc, rr, beta)`, `implicit_reward(logp, ref_logp, beta)`, `TablePolicy(n_prompts, k)`,
`train_dpo(policy, ref, prefs, beta, steps, lr)`, `aggregate_prm(steps, mode)`, `first_bad_step(steps, threshold)`.

## Friday design (45 min)

`design.md`: reward model training and preference data pipeline. Timer, `my_design.md`, `rubric.md`,
model answer on `solutions`.

## Staff angle

DPO vs RLHF-with-PPO is a cost/control trade-off, not a fashion choice: DPO is offline, cheap,
stable, but limited to the preference data's distribution; online methods (PPO, GRPO, online/iterative
DPO) explore and need a reward signal at training time. For agents, process supervision and
verifiable rewards (tests pass, tool call succeeded) are increasingly the practical signal. A staff
engineer picks based on what reward is available and trustworthy.
