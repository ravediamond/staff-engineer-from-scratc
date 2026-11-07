# Week 8: reward models

Reward models sit where your two worlds meet: they are **evaluation turned into a training
signal**. Everything you know about judges, calibration and bias reappears, except now an
optimiser is actively searching for the RM's mistakes. This week builds the core on CPU with
tiny PyTorch models: Bradley–Terry, pairwise RM training, calibration and length bias,
best-of-N over-optimisation (Goodhart, measured), and DPO plus process rewards.

Primer: `knowledge/08-reward-models-and-preference-learning.md`.
Your paper library: Robometer (trajectory-comparison reward models) and LeWM-as-reward are worked
examples of the same ideas in robotics.

| Day | Lab | Review bug |
|---|---|---|
| d1 | Bradley–Terry strengths, Elo, log-likelihood | win probability has the sign flipped |
| d2 | pairwise reward model in PyTorch, prompt-level split | split by pair leaks prompts into test |
| d3 | RM calibration (ECE, temperature) and length bias | ECE averages bins without weighting |
| d4 | best-of-N, KL of BoN, over-optimisation curve | evaluates the selected sample with the proxy RM |
| d5 | DPO from scratch, process vs outcome rewards + **Friday design** | DPO loss forgets the reference model |
