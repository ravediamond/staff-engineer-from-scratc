# W8 D2: training a pairwise reward model

Primer: `knowledge/08-reward-models-and-preference-learning.md` §2.

## The one idea

Data: triples `(prompt, chosen, rejected)`. Model: `f_θ(prompt, response) → scalar`. Loss:

```
L = −mean log σ( f_θ(x, y_c) − f_θ(x, y_r) )
```

At initialisation both rewards are about equal, so L ≈ log 2 ≈ 0.693: a step-0 sanity check you
should always print. The metric is **pairwise accuracy** on held-out pairs (fraction where
`f(chosen) > f(rejected)`). Real RMs land around 65–75% on human data, because humans disagree.

**Split by prompt, never by pair.** Several pairs share a prompt; if some go to train and others to
test, the model memorises prompt-specific features and test accuracy is inflated (leakage).

Today the "prompt + response" is a synthetic feature vector, and the hidden "true" reward is a
nonlinear function of it; preferences are sampled from Bradley–Terry on the true reward. That
keeps the lab on CPU while keeping every real failure mode.

## Today's build (`w8d2_rm.py`)

`make_preference_data` is provided. You write: `split_by_prompt`, `RewardModel` (MLP → scalar),
`pairwise_loss`, `pair_accuracy`, `train_rm`.

## Staff angle

The staff questions about an RM are about data: who labelled, with what guidelines, what is the
inter-annotator agreement (the accuracy ceiling), how prompts were sampled, how many pairs per
prompt, how ties were handled. A 2-point RM accuracy gain from a bigger model is often smaller than
the gain from removing the 15% of pairs where annotators disagree.
