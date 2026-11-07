"""W9 D2: data-parallel training with torch.distributed (gloo, CPU) that matches single-process training exactly."""
import math
import os

import torch
import torch.distributed as dist
import torch.multiprocessing as mp
from torch import nn


def shard_indices(n: int, world: int, rank: int, seed: int, epoch: int) -> list:
    """Permutation of range(n) from torch.Generator seeded with seed + epoch; pad by repeating from the start
    until the length is a multiple of world; return perm[rank::world] as a Python list."""
    g = torch.Generator().manual_seed(seed + epoch)
    perm = torch.randperm(n, generator=g).tolist()
    total = math.ceil(n / world) * world
    perm += perm[: total - n]
    return perm[rank::world]


def make_data(seed: int = 0, n: int = 256, d: int = 8) -> tuple:
    """Provided: linear regression data."""
    g = torch.Generator().manual_seed(seed)
    X = torch.randn(n, d, generator=g)
    w = torch.randn(d, 1, generator=g)
    y = X @ w + 0.1 * torch.randn(n, 1, generator=g)
    return X, y


def make_model(seed: int = 0) -> nn.Module:
    torch.manual_seed(seed)
    return nn.Linear(8, 1)


def global_batch_rows(step: int, global_batch: int, n: int) -> torch.Tensor:
    """Rows of the global batch at `step`: contiguous, wrapping around n."""
    return (torch.arange(global_batch) + step * global_batch) % n


def average_gradients(model: nn.Module, world: int) -> None:
    """all_reduce(SUM) every parameter's grad, then divide by world, in place."""
    for p in model.parameters():
        if p.grad is not None:
            dist.all_reduce(p.grad, op=dist.ReduceOp.SUM)
            p.grad /= world


def train_single(steps: int, global_batch: int, lr: float) -> torch.Tensor:
    """SGD on MSE (mean over the global batch). Return the flattened final parameters (weight then bias)."""
    X, y = make_data()
    model = make_model()
    opt = torch.optim.SGD(model.parameters(), lr=lr)
    for step in range(steps):
        rows = global_batch_rows(step, global_batch, len(X))
        opt.zero_grad()
        nn.functional.mse_loss(model(X[rows]), y[rows]).backward()
        opt.step()
    return torch.cat([p.detach().flatten() for p in model.parameters()])


def ddp_worker(rank: int, world: int, init_file: str, out_file: str, steps: int, global_batch: int,
               lr: float) -> None:
    """Join the group (gloo, init_method=f"file://{init_file}"), train on this rank's contiguous slice of each
    global batch (global_batch // world rows), average gradients, step. Rank 0 saves the flattened final
    parameters with torch.save(out_file). Always destroy the process group at the end."""
    os.environ.setdefault("GLOO_SOCKET_IFNAME", "lo0" if os.uname().sysname == "Darwin" else "lo")
    dist.init_process_group("gloo", init_method=f"file://{init_file}", rank=rank, world_size=world)
    try:
        X, y = make_data()
        model = make_model()
        opt = torch.optim.SGD(model.parameters(), lr=lr)
        local = global_batch // world
        for step in range(steps):
            rows = global_batch_rows(step, global_batch, len(X))[rank * local:(rank + 1) * local]
            opt.zero_grad()
            nn.functional.mse_loss(model(X[rows]), y[rows]).backward()
            average_gradients(model, world)
            opt.step()
        if rank == 0:
            torch.save(torch.cat([p.detach().flatten() for p in model.parameters()]), out_file)
    finally:
        dist.destroy_process_group()


def run_ddp(world: int, steps: int, global_batch: int, lr: float, tmpdir: str) -> torch.Tensor:
    """Provided: spawn `world` processes running ddp_worker and return rank 0's saved parameters."""
    init_file = os.path.join(tmpdir, "init")
    out_file = os.path.join(tmpdir, "out.pt")
    mp.spawn(ddp_worker, args=(world, init_file, out_file, steps, global_batch, lr), nprocs=world, join=True)
    return torch.load(out_file)
