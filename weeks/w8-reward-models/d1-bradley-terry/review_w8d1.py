"""Review: arena leaderboard code. The model everyone agrees is worst ended up on top.
Find the bug, fix it, explain:

WHY:
"""
import torch


def win_prob(r, i, j):
    """P(i beats j) under Bradley-Terry."""
    return torch.sigmoid(r[j] - r[i])


def fit(n, comparisons, steps=300, lr=0.05):
    r = torch.zeros(n, requires_grad=True)
    opt = torch.optim.Adam([r], lr=lr)
    for _ in range(steps):
        opt.zero_grad()
        loss = -sum(torch.log(win_prob(r, w, l)) for w, l in comparisons) / len(comparisons) + 1e-3 * (r ** 2).sum()
        loss.backward()
        opt.step()
    return r.detach()
