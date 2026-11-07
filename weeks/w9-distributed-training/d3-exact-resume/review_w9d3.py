"""Review: checkpoint code from the training repo. After every preemption the loss spikes for ~50 steps.
Find the bug, fix it, explain:

WHY:
"""
import torch


def save(path, model, opt, step):
    torch.save({"model": model.state_dict(), "step": step}, path)


def load(path, model, opt):
    blob = torch.load(path)
    model.load_state_dict(blob["model"])
    if "opt" in blob:
        opt.load_state_dict(blob["opt"])
    return blob["step"]
