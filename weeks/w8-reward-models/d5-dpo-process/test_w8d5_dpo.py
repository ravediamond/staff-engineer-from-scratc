import copy
import math

import pytest
import torch

from w8d5_dpo import TablePolicy, aggregate_prm, dpo_loss, first_bad_step, implicit_reward, train_dpo


def test_loss_is_log2_at_reference():
    lp = torch.tensor([-1.0, -3.0, -0.2])
    lr_ = torch.tensor([-2.0, -0.5, -4.0])
    assert dpo_loss(lp, lr_, lp, lr_, beta=0.5).item() == pytest.approx(math.log(2))


def test_loss_direction():
    ref_c = torch.tensor([-2.0])
    ref_r = torch.tensor([-2.0])
    better = dpo_loss(torch.tensor([-1.0]), torch.tensor([-3.0]), ref_c, ref_r, 1.0)
    worse = dpo_loss(torch.tensor([-3.0]), torch.tensor([-1.0]), ref_c, ref_r, 1.0)
    assert better.item() < math.log(2) < worse.item()
    assert implicit_reward(torch.tensor([-1.0]), torch.tensor([-2.0]), 0.1).item() == pytest.approx(0.1)


def test_table_policy_logp_uniform():
    pol = TablePolicy(3, 4)
    out = pol.logp(torch.tensor([0, 2]), torch.tensor([1, 3]))
    assert torch.allclose(out, torch.full((2,), math.log(0.25)))


def test_train_dpo_moves_mass_to_chosen():
    torch.manual_seed(0)
    policy = TablePolicy(5, 4)
    ref = copy.deepcopy(policy)
    prefs = [(p, 0, j) for p in range(5) for j in (1, 2, 3)]
    hist = train_dpo(policy, ref, prefs, beta=0.5, steps=150, lr=0.1)
    assert hist[0] == pytest.approx(math.log(2), abs=1e-6)
    assert hist[-1] < 0.2
    probs = torch.softmax(policy.logits, dim=-1)
    assert (probs[:, 0] > 0.6).all()
    assert torch.equal(ref.logits, torch.zeros(5, 4)), "reference must stay frozen"


def test_prm():
    s = [0.9, 0.95, 0.3, 0.9]
    assert aggregate_prm(s, "min") == 0.3
    assert aggregate_prm(s, "product") == pytest.approx(0.9 * 0.95 * 0.3 * 0.9)
    assert aggregate_prm(s, "last") == 0.9
    assert first_bad_step(s, 0.5) == 2 and first_bad_step(s, 0.1) is None
