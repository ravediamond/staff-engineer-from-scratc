"""W8 D3: calibration (ECE, temperature scaling) and length bias of a reward model."""
import math

import torch


def ece(probs: list, labels: list, n_bins: int = 10) -> float:
    """probs: predicted P(label == 1). labels: 0/1. Equal-width bins on [0, 1] (p == 1.0 goes to the last bin).
    confidence = prob, accuracy = label mean. ECE = sum_b n_b / N * |acc_b - conf_b|, empty bins skipped."""
    # TODO
    raise NotImplementedError


def nll(margins: torch.Tensor, labels: torch.Tensor, T: float) -> float:
    """Mean binary cross-entropy of sigmoid(margins / T) against labels."""
    # TODO
    raise NotImplementedError


def fit_temperature(margins: torch.Tensor, labels: torch.Tensor, steps: int = 300, lr: float = 0.05) -> float:
    """Fit T > 0 by optimising log_T (init 0) with Adam on the NLL. Return T as a float."""
    # TODO
    raise NotImplementedError


def pearson(x: list, y: list) -> float:
    # TODO
    raise NotImplementedError


def length_bias(rewards: list, lengths: list) -> float:
    """Pearson correlation between reward and length (call on responses of equal true quality)."""
    # TODO
    raise NotImplementedError
