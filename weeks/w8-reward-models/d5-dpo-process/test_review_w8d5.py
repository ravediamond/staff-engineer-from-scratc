import math

import torch

from review_w8d5 import dpo_loss


def test_review_reference_matters():
    pi_c, pi_r = torch.tensor([-1.0]), torch.tensor([-5.0])
    assert abs(dpo_loss(pi_c, pi_r, pi_c, pi_r).item() - math.log(2)) < 1e-6
