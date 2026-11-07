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
    d = _step_dir(root, step)
    os.makedirs(d, exist_ok=True)
    path = os.path.join(d, f"shard-{rank}-of-{world}.pt")
    torch.save(tensor, path + ".tmp")
    os.replace(path + ".tmp", path)
    return path


def write_manifest(root: str, step: int, world: int) -> None:
    """After all shards exist: manifest.json = {"step", "world", "shards": {filename: sha256}}, written atomically."""
    d = _step_dir(root, step)
    shards = {f"shard-{r}-of-{world}.pt": _sha256(os.path.join(d, f"shard-{r}-of-{world}.pt")) for r in range(world)}
    tmp = os.path.join(d, "manifest.json.tmp")
    with open(tmp, "w") as f:
        json.dump({"step": step, "world": world, "shards": shards}, f)
    os.replace(tmp, os.path.join(d, "manifest.json"))


def is_complete(root: str, step: int) -> bool:
    """Manifest exists and every listed shard exists with a matching checksum."""
    d = _step_dir(root, step)
    mpath = os.path.join(d, "manifest.json")
    if not os.path.exists(mpath):
        return False
    with open(mpath) as f:
        man = json.load(f)
    for name, digest in man["shards"].items():
        p = os.path.join(d, name)
        if not os.path.exists(p) or _sha256(p) != digest:
            return False
    return True


def latest_complete(root: str):
    """Highest step whose checkpoint is complete, or None."""
    if not os.path.isdir(root):
        return None
    steps = sorted((int(n.split("-")[1]) for n in os.listdir(root) if n.startswith("step-")), reverse=True)
    for s in steps:
        if is_complete(root, s):
            return s
    return None


def load_full(root: str, step: int) -> torch.Tensor:
    """Concatenate shards 0..world-1 (world from the manifest)."""
    d = _step_dir(root, step)
    with open(os.path.join(d, "manifest.json")) as f:
        world = json.load(f)["world"]
    return torch.cat([torch.load(os.path.join(d, f"shard-{r}-of-{world}.pt")) for r in range(world)])


def reshard(full: torch.Tensor, new_world: int) -> list:
    """Split a flat tensor into new_world contiguous shards; the first len % new_world shards get one extra element."""
    base, extra = divmod(len(full), new_world)
    sizes = [base + (1 if i < extra else 0) for i in range(new_world)]
    return list(torch.split(full, sizes))


def mfu(params: float, tokens_per_s: float, n_gpus: int, peak_flops: float) -> float:
    return 6 * params * tokens_per_s / (n_gpus * peak_flops)


def goodput(useful_seconds: float, wall_seconds: float) -> float:
    return useful_seconds / wall_seconds
