import torch

from review_w9d2 import sync


def test_review_mean_not_sum():
    g = [torch.tensor([1.0, 2.0]), torch.tensor([3.0, 4.0]), torch.tensor([5.0, 6.0]), torch.tensor([7.0, 8.0])]
    out = sync(g)
    assert all(torch.allclose(o, torch.tensor([4.0, 5.0])) for o in out)
