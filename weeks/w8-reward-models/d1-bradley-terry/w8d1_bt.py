"""W8 D1: Bradley-Terry fitted with PyTorch, plus Elo."""
import torch


def bt_prob(r: torch.Tensor, i: int, j: int) -> torch.Tensor:
    """P(i beats j) = sigmoid(r_i - r_j)."""
    # TODO
    raise NotImplementedError


def bt_log_likelihood(r: torch.Tensor, comparisons: list) -> torch.Tensor:
    """Sum over (winner, loser) of log sigmoid(r_w - r_l). Use torch.nn.functional.logsigmoid (stable)."""
    # TODO
    raise NotImplementedError


def bt_fit(n_items: int, comparisons: list, steps: int = 500, lr: float = 0.05, l2: float = 1e-3,
           seed: int = 0) -> torch.Tensor:
    """Minimise -loglik/len(comparisons) + l2 * sum(r^2) with Adam from zeros. Return r - r.mean(), detached."""
    # TODO
    raise NotImplementedError


def elo_expected(ra: float, rb: float) -> float:
    # TODO
    raise NotImplementedError


def elo_update(ra: float, rb: float, score_a: float, k: float = 32) -> tuple:
    """score_a: 1 win, 0.5 draw, 0 loss. Return new (ra, rb); zero-sum."""
    # TODO
    raise NotImplementedError
