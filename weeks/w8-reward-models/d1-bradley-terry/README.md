# W8 D1: Bradley–Terry and Elo

Primer: `knowledge/08-reward-models-and-preference-learning.md` §1.

## The one idea

Humans are bad at absolute scores and decent at comparisons. **Bradley–Terry** turns pairwise
comparisons into latent strengths: `P(i beats j) = σ(r_i − r_j)`. Fit `r` by maximising the
log-likelihood of observed outcomes, `Σ log σ(r_winner − r_loser)`, with a small L2 penalty (the
model is shift-invariant: only differences matter, so centre `r` at mean 0).

A **reward model** is Bradley–Terry where `r_i` is not a free parameter per item but the output of a
network: `r = f_θ(prompt, response)`. Same loss (D2).

**Elo** (chess, Chatbot Arena's original leaderboard) is online stochastic gradient ascent on the same
model in base 10: `E_a = 1 / (1 + 10^((R_b − R_a)/400))`, `R_a += K·(S_a − E_a)`. Order-dependent;
modern leaderboards fit BT offline on all comparisons instead.

## Today's build (`w8d1_bt.py`, PyTorch)

`bt_prob(r, i, j)`, `bt_log_likelihood(r, comparisons)`, `bt_fit(n_items, comparisons, steps, lr, l2)` → centred
tensor of strengths (Adam on the negative log-likelihood), `elo_expected(ra, rb)`, `elo_update(ra, rb, score_a, k)`.

## Staff angle

Leaderboards built on comparisons hide three decisions a staff engineer should surface: which
prompts were compared (distribution), who judged (humans, which humans, or an LLM), and how
uncertainty is reported (bootstrap CIs on strengths: two models 5 Elo apart are tied). The
same questions apply to every internal "model A vs model B" bake-off you will run.
