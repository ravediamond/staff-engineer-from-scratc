import torch

from w9d2_ddp import run_ddp, shard_indices, train_single


def test_shard_indices_partition():
    n, world = 10, 4
    shards = [shard_indices(n, world, r, seed=1, epoch=0) for r in range(world)]
    assert all(len(s) == 3 for s in shards)
    flat = sum(shards, [])
    assert set(flat) == set(range(10)) and len(flat) == 12
    assert shard_indices(n, world, 0, 1, 0) == shards[0], "deterministic"
    assert shard_indices(n, world, 0, 1, 1) != shards[0], "epoch changes the permutation"


def test_ddp_matches_single_process(tmp_path):
    single = train_single(steps=30, global_batch=32, lr=0.1)
    ddp = run_ddp(world=2, steps=30, global_batch=32, lr=0.1, tmpdir=str(tmp_path))
    assert torch.allclose(single, ddp, atol=1e-6), (single, ddp)
