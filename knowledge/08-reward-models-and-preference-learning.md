# 08. Reward models and preference learning

## §1 Bradley–Terry

`P(i ≻ j) = σ(r_i − r_j)`; fit by maximum likelihood with a small L2; shift-invariant. Elo is online SGD on
the same model. Report bootstrap CIs; control for style and length when ranking models.

## §2 Pairwise reward models

`L = −log σ(r(x, y_c) − r(x, y_r))`, step-0 loss log 2. Split by prompt. Accuracy is bounded by inter-annotator
agreement. Data quality (guidelines, overlap, gold items, tie handling) dominates model size.

## §3 Calibration and bias

ECE weighted by bin size; temperature scaling preserves ranking; length bias measured on equal-quality pairs and
removed by balanced data or covariates. Calibration matters when scores become thresholds.

## §4 Over-optimisation

Best-of-N with `KL = log N − (N−1)/N`; proxy reward rises monotonically, gold reward rises then falls (Gao et al.,
2022). Never evaluate with the selecting RM. Mitigations: KL penalty, ensembles, fresh data on current policy
outputs, early stopping on gold or judge metrics.

## §5 DPO and friends

DPO turns the KL-regularised objective into a classification loss on preferences using
`β log(π/π_ref)` as the implicit reward; step-0 loss log 2; β ≈ KL strength. Offline, stable, cheap; limited to the
data's distribution. Variants: IPO, KTO (unpaired good/bad labels), ORPO (no reference model), online/iterative DPO.
RL methods (PPO, GRPO) when a reliable reward exists and exploration matters.

## §6 Process rewards and verifiable rewards

PRMs score steps (min/product aggregation, first bad step localisation); outcome RMs score final answers.
Verifiable rewards (tests, exact answers, checkers) power RL for reasoning models; their failure mode is
checker gaps.

## Questions

1. How would you know your RM is good enough to optimise against?
<details><summary>Answer</summary>Held-out accuracy near the human agreement ceiling on prompts from the target distribution, sliced; calibration; bias probes (length, style, sycophancy, adversarial padding); and above all, a BoN or short-RL experiment where gold (human or independent judge) quality improves with optimization pressure up to the intended operating point.</details>

2. Why does RLHF need a KL penalty?
<details><summary>Answer</summary>The RM is only accurate near the distribution it was trained on. Unconstrained optimization drifts into regions where RM errors dominate (reward hacking) and destroys capabilities and fluency learned in pretraining. The KL to the reference keeps the policy close to where the reward is trustworthy.</details>

3. Robotics connection: how is a learned reward for robot trajectories (e.g. trajectory-comparison models) similar to RLHF RMs, and what is extra hard?
<details><summary>Answer</summary>Same structure: preferences or comparisons between trajectories trained with a BT-style loss, then used to rank, filter, or as an RL reward. Extra hard: long horizons and credit assignment, partial observability, embodiment and camera shifts, and exploitation by physical policies (shortcuts the reward does not penalize), so progress-based and process-style rewards, plus real-world verification, matter more.</details>
