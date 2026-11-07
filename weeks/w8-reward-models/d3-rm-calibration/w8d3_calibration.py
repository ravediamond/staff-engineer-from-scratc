"""W8 D3: calibration (ECE, temperature scaling) and length bias of a reward model."""
import math

import torch


def ece(probs: list, labels: list, n_bins: int = 10) -> float:
    """probs: predicted P(label == 1). labels: 0/1. Equal-width bins on [0, 1] (p == 1.0 goes to the last bin).
    confidence = prob, accuracy = label mean. ECE = sum_b n_b / N * |acc_b - conf_b|, empty bins skipped."""
    n = len(probs)
    bins = [[] for _ in range(n_bins)]
    for p, y in zip(probs, labels):
        bins[min(int(p * n_bins), n_bins - 1)].append((p, y))
    total = 0.0
    for b in bins:
        if b:
            conf = sum(p for p, _ in b) / len(b)
            acc = sum(y for _, y in b) / len(b)
            total += len(b) / n * abs(acc - conf)
    return total


def nll(margins: torch.Tensor, labels: torch.Tensor, T: float) -> float:
    """Mean binary cross-entropy of sigmoid(margins / T) against labels."""
    return torch.nn.functional.binary_cross_entropy_with_logits(margins / T, labels.float()).item()


def fit_temperature(margins: torch.Tensor, labels: torch.Tensor, steps: int = 300, lr: float = 0.05) -> float:
    """Fit T > 0 by optimising log_T (init 0) with Adam on the NLL. Return T as a float."""
    log_t = torch.zeros(1, requires_grad=True)
    opt = torch.optim.Adam([log_t], lr=lr)
    y = labels.float()
    for _ in range(steps):
        opt.zero_grad()
        loss = torch.nn.functional.binary_cross_entropy_with_logits(margins / log_t.exp(), y)
        loss.backward()
        opt.step()
    return log_t.exp().item()


def pearson(x: list, y: list) -> float:
    n = len(x)
    mx, my = sum(x) / n, sum(y) / n
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    sxx = sum((a - mx) ** 2 for a in x)
    syy = sum((b - my) ** 2 for b in y)
    return sxy / math.sqrt(sxx * syy)


def length_bias(rewards: list, lengths: list) -> float:
    """Pearson correlation between reward and length (call on responses of equal true quality)."""
    return pearson(rewards, lengths)
