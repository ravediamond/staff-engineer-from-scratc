import os

import pytest
import torch

from w9d5_ckpt import goodput, is_complete, latest_complete, load_full, mfu, reshard, save_shard, write_manifest


def save_step(root, step, full, world):
    for r, shard in enumerate(reshard(full, world)):
        save_shard(root, step, r, world, shard)
    write_manifest(root, step, world)


def test_roundtrip_and_reshard(tmp_path):
    root = str(tmp_path)
    full = torch.arange(23, dtype=torch.float32)
    save_step(root, 100, full, world=4)
    assert is_complete(root, 100)
    assert torch.equal(load_full(root, 100), full)
    new = reshard(load_full(root, 100), 3)
    assert [len(s) for s in new] == [8, 8, 7] and torch.equal(torch.cat(new), full)


def test_incomplete_steps_are_skipped(tmp_path):
    root = str(tmp_path)
    full = torch.randn(40)
    save_step(root, 100, full, 4)
    for r, shard in enumerate(reshard(full * 2, 4)[:3]):  # step 200: node 3 died, no manifest
        save_shard(root, 200, r, 4, shard)
    save_step(root, 300, full * 3, 4)
    os.remove(os.path.join(root, "step-000300", "shard-2-of-4.pt"))  # manifest present, shard lost
    assert not is_complete(root, 200) and not is_complete(root, 300)
    assert latest_complete(root) == 100


def test_corrupted_shard_detected(tmp_path):
    root = str(tmp_path)
    save_step(root, 5, torch.randn(10), 2)
    torch.save(torch.zeros(5), os.path.join(root, "step-000005", "shard-1-of-2.pt"))
    assert not is_complete(root, 5) and latest_complete(root) is None


def test_mfu_goodput():
    assert mfu(7e9, 2.5e6, 1000, 990e12) == pytest.approx(0.106, abs=1e-3)
    assert goodput(3000, 3600) == pytest.approx(5 / 6)
