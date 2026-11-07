"""W9 D3: checkpoint/restore everything that affects the future, then prove resume is bit-exact."""
import os
import random

import numpy as np
import torch
from torch import nn


def build(seed: int = 0) -> dict:
    """Provided: model with dropout, Adam, cosine scheduler, step counter. Seeds all RNGs."""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    model = nn.Sequential(nn.Linear(6, 32), nn.ReLU(), nn.Dropout(0.2), nn.Linear(32, 1))
    opt = torch.optim.Adam(model.parameters(), lr=1e-2)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=50)
    return {"model": model, "opt": opt, "sched": sched, "step": 0}


def train_steps(state: dict, n: int) -> list:
    """Provided: deliberately uses all three RNGs (python for noise level, numpy for data, torch for dropout)."""
    model, opt, sched = state["model"], state["opt"], state["sched"]
    losses = []
    model.train()
    for _ in range(n):
        noise = random.uniform(0.0, 0.1)
        x = torch.from_numpy(np.random.randn(16, 6).astype(np.float32))
        y = x.sum(dim=1, keepdim=True) + noise
        loss = nn.functional.mse_loss(model(x), y)
        opt.zero_grad()
        loss.backward()
        opt.step()
        sched.step()
        state["step"] += 1
        losses.append(loss.item())
    return losses


def save_checkpoint(path: str, state: dict) -> None:
    """Save model, optimizer, scheduler, step, and the torch / numpy / python RNG states.
    Atomic: torch.save to path + ".tmp", then os.replace."""
    # TODO
    raise NotImplementedError


def load_checkpoint(path: str, seed: int = 0) -> dict:
    """Rebuild a fresh state with build(seed), then restore everything saved (RNGs LAST, after build seeded them).
    torch.load(..., weights_only=False) because the blob contains numpy and python objects."""
    # TODO
    raise NotImplementedError


def params_vector(state: dict) -> torch.Tensor:
    return torch.cat([p.detach().flatten() for p in state["model"].parameters()])
