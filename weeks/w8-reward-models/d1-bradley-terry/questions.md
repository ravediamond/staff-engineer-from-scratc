# Questions

1. Write the Bradley–Terry likelihood. Why is the model shift-invariant, and what do you do about it?
2. Elo vs offline BT fit: why did leaderboards move to BT?
3. How do you put confidence intervals on BT strengths?
4. Two models differ by 8 points on an arena leaderboard. What do you need before calling a winner?
5. How is a reward model "Bradley–Terry with a network"?

## Model answers

1. L(r) = Π σ(r_w − r_l) over comparisons. Only differences enter, so adding a constant to all r leaves L unchanged and the MLE is defined up to a shift. Fix by centering (mean 0), pinning one item to 0, or an L2 prior (which also handles undefeated items).
2. Elo is online and order-dependent: the same games in a different order give different ratings, and K trades responsiveness against noise. A BT fit on all comparisons is order-free, has a proper likelihood (CIs, tie models, covariates such as style or length control), and is the MLE of the same model.
3. Bootstrap the comparisons (resample battles, refit, take percentiles), or use the inverse Hessian of the negative log-likelihood (Fisher information) for approximate standard errors.
4. Overlapping bootstrap CIs mean "statistically tied". Check the prompt distribution (does it match my use case?), style or length confounds (style-controlled ranking), and the number of comparisons per model. 8 Elo ≈ 51% win probability, which is practically indistinguishable.
5. Instead of a free r per item, r = f_θ(prompt, response); training minimizes −log σ(f_θ(x, y_chosen) − f_θ(x, y_rejected)), which is exactly the BT negative log-likelihood with shared parameters, so it generalizes to unseen responses.
