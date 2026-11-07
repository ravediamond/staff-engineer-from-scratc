import os

import torch

from w9d3_resume import build, load_checkpoint, params_vector, save_checkpoint, train_steps


def test_resume_is_bit_exact(tmp_path):
    ref = build(0)
    ref_losses = train_steps(ref, 20)

    a = build(0)
    first = train_steps(a, 10)
    ck = str(tmp_path / "ckpt.pt")
    save_checkpoint(ck, a)
    del a
    train_steps(build(123), 7)  # pollute global RNG state, as a fresh process would differ
    b = load_checkpoint(ck, seed=0)
    second = train_steps(b, 10)

    assert first + second == ref_losses
    assert torch.equal(params_vector(b), params_vector(ref))
    assert b["step"] == 20
    assert b["sched"].get_last_lr() == ref["sched"].get_last_lr()


def test_atomic_save_leaves_no_tmp(tmp_path):
    s = build(0)
    p = str(tmp_path / "c.pt")
    save_checkpoint(p, s)
    assert os.path.exists(p) and not os.path.exists(p + ".tmp")
