import math

import torch

from w8d2_rm import RewardModel, make_preference_data, pair_accuracy, pairwise_loss, split_by_prompt, train_rm


def test_split_by_prompt_no_leak():
    data = make_preference_data(100, 5)
    tr, te = split_by_prompt(data, 0.2, seed=3)
    ptr, pte = {d["prompt_id"] for d in tr}, {d["prompt_id"] for d in te}
    assert not (ptr & pte) and len(pte) == 20 and len(tr) + len(te) == len(data)


def test_model_shape_and_step0_loss():
    torch.manual_seed(0)
    m = RewardModel(32)
    x = torch.randn(7, 32)
    assert m(x).shape == (7,)
    z = torch.zeros(5)
    assert abs(pairwise_loss(z, z).item() - math.log(2)) < 1e-6
    assert pairwise_loss(torch.tensor([5.0]), torch.tensor([0.0])).item() < 0.01


def test_training_generalises_to_new_prompts():
    torch.manual_seed(0)
    data = make_preference_data(400, 6)
    tr, te = split_by_prompt(data, 0.25)
    m = RewardModel(32)
    hist = train_rm(m, tr, epochs=25)
    assert hist[-1] < hist[0] < 0.75
    acc = pair_accuracy(m, te)
    assert acc > 0.72, acc
