"""W8 D5: DPO on a tabular policy, and process-reward aggregation."""
import math

import torch
from torch import nn


def dpo_loss(pi_c: torch.Tensor, pi_r: torch.Tensor, ref_c: torch.Tensor, ref_r: torch.Tensor,
             beta: float) -> torch.Tensor:
    """Inputs: log-probs (B,). -mean logsigmoid(beta * ((pi_c - ref_c) - (pi_r - ref_r)))."""
    # TODO
    raise NotImplementedError


def implicit_reward(logp: torch.Tensor, ref_logp: torch.Tensor, beta: float) -> torch.Tensor:
    # TODO
    raise NotImplementedError


class TablePolicy(nn.Module):
    """logits: (n_prompts, k) parameter initialised to zeros (uniform policy)."""

    def __init__(self, n_prompts: int, k: int):
        super().__init__()
        self.logits = nn.Parameter(torch.zeros(n_prompts, k))

    def logp(self, prompts: torch.Tensor, responses: torch.Tensor) -> torch.Tensor:
        """log pi(response | prompt) for index tensors (B,) -> (B,)."""
        # TODO
        raise NotImplementedError


def train_dpo(policy: TablePolicy, ref: TablePolicy, prefs: list, beta: float = 0.1, steps: int = 200,
              lr: float = 0.1) -> list:
    """prefs: [(prompt, chosen_idx, rejected_idx)]. Full-batch Adam on dpo_loss; ref is frozen
    (compute its log-probs under torch.no_grad()). Return the loss history."""
    # TODO
    raise NotImplementedError


def aggregate_prm(step_scores: list, mode: str) -> float:
    """mode: 'min' | 'product' | 'last'."""
    # TODO
    raise NotImplementedError


def first_bad_step(step_scores: list, threshold: float):
    """Index of the first step with score < threshold, or None."""
    # TODO
    raise NotImplementedError
