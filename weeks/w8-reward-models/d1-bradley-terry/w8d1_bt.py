"""W8 D1: Bradley-Terry fitted with PyTorch, plus Elo."""
import torch


def bt_prob(r: torch.Tensor, i: int, j: int) -> torch.Tensor:
    """P(i beats j) = sigmoid(r_i - r_j)."""
    return torch.sigmoid(r[i] - r[j])


def bt_log_likelihood(r: torch.Tensor, comparisons: list) -> torch.Tensor:
    """Sum over (winner, loser) of log sigmoid(r_w - r_l). Use torch.nn.functional.logsigmoid (stable)."""
    w = torch.tensor([c[0] for c in comparisons])
    l = torch.tensor([c[1] for c in comparisons])
    return torch.nn.functional.logsigmoid(r[w] - r[l]).sum()


def bt_fit(n_items: int, comparisons: list, steps: int = 500, lr: float = 0.05, l2: float = 1e-3,
           seed: int = 0) -> torch.Tensor:
    """Minimise -loglik/len(comparisons) + l2 * sum(r^2) with Adam from zeros. Return r - r.mean(), detached."""
    torch.manual_seed(seed)
    r = torch.zeros(n_items, requires_grad=True)
    opt = torch.optim.Adam([r], lr=lr)
    for _ in range(steps):
        opt.zero_grad()
        loss = -bt_log_likelihood(r, comparisons) / len(comparisons) + l2 * (r ** 2).sum()
        loss.backward()
        opt.step()
    r = r.detach()
    return r - r.mean()


def elo_expected(ra: float, rb: float) -> float:
    return 1.0 / (1.0 + 10 ** ((rb - ra) / 400))


def elo_update(ra: float, rb: float, score_a: float, k: float = 32) -> tuple:
    """score_a: 1 win, 0.5 draw, 0 loss. Return new (ra, rb); zero-sum."""
    ea = elo_expected(ra, rb)
    delta = k * (score_a - ea)
    return ra + delta, rb - delta
