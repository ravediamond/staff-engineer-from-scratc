"""W9 D5: sharded checkpoints with a manifest written last, crash-safe loading, resharding, MFU."""
import hashlib
import json
import os

import torch


def _step_dir(root: str, step: int) -> str:
    return os.path.join(root, f"step-{step:06d}")


def _sha256(path: str) -> str:
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def save_shard(root: str, step: int, rank: int, world: int, tensor: torch.Tensor) -> str:
    """Write shard-{rank}-of-{world}.pt atomically into the step dir (create it). Return the path."""
    # TODO
    raise NotImplementedError


def write_manifest(root: str, step: int, world: int) -> None:
    """After all shards exist: manifest.json = {"step", "world", "shards": {filename: sha256}}, written atomically."""
    # TODO
    raise NotImplementedError


def is_complete(root: str, step: int) -> bool:
    """Manifest exists and every listed shard exists with a matching checksum."""
    # TODO
    raise NotImplementedError


def latest_complete(root: str):
    """Highest step whose checkpoint is complete, or None."""
    # TODO
    raise NotImplementedError


def load_full(root: str, step: int) -> torch.Tensor:
    """Concatenate shards 0..world-1 (world from the manifest)."""
    # TODO
    raise NotImplementedError


def reshard(full: torch.Tensor, new_world: int) -> list:
    """Split a flat tensor into new_world contiguous shards; the first len % new_world shards get one extra element."""
    # TODO
    raise NotImplementedError


def mfu(params: float, tokens_per_s: float, n_gpus: int, peak_flops: float) -> float:
    # TODO
    raise NotImplementedError


def goodput(useful_seconds: float, wall_seconds: float) -> float:
    # TODO
    raise NotImplementedError
