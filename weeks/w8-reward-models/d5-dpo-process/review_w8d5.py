"""Review: DPO loss from a fine-tuning repo. Training 'works' (loss goes down) but the model drifts far from
the base model and gets weird. Find the bug, fix it, explain:

WHY:
"""
import torch
from torch import nn


def dpo_loss(pi_c, pi_r, ref_c, ref_r, beta=0.1):
    return -nn.functional.logsigmoid(beta * (pi_c - pi_r)).mean()
