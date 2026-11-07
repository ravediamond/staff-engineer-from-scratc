"""W8 D2: pairwise reward model on synthetic preference data (PyTorch, CPU)."""
import random

import torch
from torch import nn


def make_preference_data(n_prompts: int = 300, pairs_per_prompt: int = 6, dim: int = 16, seed: int = 0) -> list:
    """Provided. Each prompt has a context vector; each response a feature vector. The input to the RM is
    concat(prompt, response) (2*dim). True reward = tanh(w1 . response) + (prompt . response) * 0.3.
    Labels sampled from Bradley-Terry on the true reward. Returns [{"prompt_id", "chosen", "rejected"}]."""
    g = torch.Generator().manual_seed(seed)
    w1 = torch.randn(dim, generator=g)
    data = []
    for p in range(n_prompts):
        ctx = torch.randn(dim, generator=g)
        for _ in range(pairs_per_prompt):
            a, b = torch.randn(dim, generator=g), torch.randn(dim, generator=g)
            ra = torch.tanh(w1 @ a) + 0.3 * (ctx @ a) / dim ** 0.5
            rb = torch.tanh(w1 @ b) + 0.3 * (ctx @ b) / dim ** 0.5
            a_wins = torch.rand(1, generator=g).item() < torch.sigmoid(3 * (ra - rb)).item()
            win, lose = (a, b) if a_wins else (b, a)
            data.append({"prompt_id": p, "chosen": torch.cat([ctx, win]), "rejected": torch.cat([ctx, lose])})
    return data


def split_by_prompt(data: list, test_frac: float, seed: int = 0) -> tuple:
    """Shuffle the distinct prompt ids with random.Random(seed), put the first round(test_frac * n_prompts)
    in test. Return (train, test) lists of pairs. No prompt may appear in both."""
    ids = sorted({d["prompt_id"] for d in data})
    random.Random(seed).shuffle(ids)
    test_ids = set(ids[: round(test_frac * len(ids))])
    return [d for d in data if d["prompt_id"] not in test_ids], [d for d in data if d["prompt_id"] in test_ids]


class RewardModel(nn.Module):
    """MLP: Linear(in_dim, hidden) -> ReLU -> Linear(hidden, hidden) -> ReLU -> Linear(hidden, 1).
    forward(x: (B, in_dim)) -> (B,) rewards."""

    def __init__(self, in_dim: int, hidden: int = 64):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(in_dim, hidden), nn.ReLU(), nn.Linear(hidden, hidden), nn.ReLU(),
                                 nn.Linear(hidden, 1))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x).squeeze(-1)  # (B,)


def pairwise_loss(r_chosen: torch.Tensor, r_rejected: torch.Tensor) -> torch.Tensor:
    """-mean(logsigmoid(r_c - r_r))."""
    return -nn.functional.logsigmoid(r_chosen - r_rejected).mean()


@torch.no_grad()
def pair_accuracy(model: nn.Module, data: list) -> float:
    model.eval()
    c = torch.stack([d["chosen"] for d in data])
    r = torch.stack([d["rejected"] for d in data])
    return (model(c) > model(r)).float().mean().item()


def train_rm(model: nn.Module, train: list, epochs: int = 30, lr: float = 3e-3, batch: int = 64,
             seed: int = 0, weight_decay: float = 1e-4) -> list:
    """AdamW, shuffled minibatches (torch.Generator seeded with seed). Return per-epoch mean training loss."""
    g = torch.Generator().manual_seed(seed)
    c = torch.stack([d["chosen"] for d in train])
    r = torch.stack([d["rejected"] for d in train])
    opt = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=weight_decay)
    history = []
    for _ in range(epochs):
        model.train()
        perm = torch.randperm(len(train), generator=g)
        total, n = 0.0, 0
        for i in range(0, len(train), batch):
            idx = perm[i:i + batch]
            loss = pairwise_loss(model(c[idx]), model(r[idx]))
            opt.zero_grad()
            loss.backward()
            opt.step()
            total += loss.item() * len(idx)
            n += len(idx)
        history.append(total / n)
    return history
