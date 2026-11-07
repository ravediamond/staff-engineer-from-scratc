"""W8 D5: DPO on a tabular policy, and process-reward aggregation."""
import math

import torch
from torch import nn


def dpo_loss(pi_c: torch.Tensor, pi_r: torch.Tensor, ref_c: torch.Tensor, ref_r: torch.Tensor,
             beta: float) -> torch.Tensor:
    """Inputs: log-probs (B,). -mean logsigmoid(beta * ((pi_c - ref_c) - (pi_r - ref_r)))."""
    return -nn.functional.logsigmoid(beta * ((pi_c - ref_c) - (pi_r - ref_r))).mean()


def implicit_reward(logp: torch.Tensor, ref_logp: torch.Tensor, beta: float) -> torch.Tensor:
    return beta * (logp - ref_logp)


class TablePolicy(nn.Module):
    """logits: (n_prompts, k) parameter initialised to zeros (uniform policy)."""

    def __init__(self, n_prompts: int, k: int):
        super().__init__()
        self.logits = nn.Parameter(torch.zeros(n_prompts, k))

    def logp(self, prompts: torch.Tensor, responses: torch.Tensor) -> torch.Tensor:
        """log pi(response | prompt) for index tensors (B,) -> (B,)."""
        lp = torch.log_softmax(self.logits[prompts], dim=-1)  # (B, k)
        return lp.gather(1, responses.unsqueeze(1)).squeeze(1)  # (B,)


def train_dpo(policy: TablePolicy, ref: TablePolicy, prefs: list, beta: float = 0.1, steps: int = 200,
              lr: float = 0.1) -> list:
    """prefs: [(prompt, chosen_idx, rejected_idx)]. Full-batch Adam on dpo_loss; ref is frozen
    (compute its log-probs under torch.no_grad()). Return the loss history."""
    p = torch.tensor([x[0] for x in prefs])
    c = torch.tensor([x[1] for x in prefs])
    r = torch.tensor([x[2] for x in prefs])
    with torch.no_grad():
        ref_c, ref_r = ref.logp(p, c), ref.logp(p, r)
    opt = torch.optim.Adam(policy.parameters(), lr=lr)
    hist = []
    for _ in range(steps):
        opt.zero_grad()
        loss = dpo_loss(policy.logp(p, c), policy.logp(p, r), ref_c, ref_r, beta)
        loss.backward()
        opt.step()
        hist.append(loss.item())
    return hist


def aggregate_prm(step_scores: list, mode: str) -> float:
    """mode: 'min' | 'product' | 'last'."""
    if mode == "min":
        return min(step_scores)
    if mode == "product":
        return math.prod(step_scores)
    if mode == "last":
        return step_scores[-1]
    raise ValueError(mode)


def first_bad_step(step_scores: list, threshold: float):
    """Index of the first step with score < threshold, or None."""
    for i, s in enumerate(step_scores):
        if s < threshold:
            return i
    return None
