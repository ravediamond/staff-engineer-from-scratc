import torch
from torch import nn

from review_w9d3 import load, save


def test_review_optimizer_state_restored(tmp_path):
    torch.manual_seed(0)
    m = nn.Linear(3, 1)
    opt = torch.optim.Adam(m.parameters(), lr=0.1)
    for _ in range(5):
        opt.zero_grad()
        m(torch.randn(4, 3)).pow(2).mean().backward()
        opt.step()
    save(str(tmp_path / "c.pt"), m, opt, 5)
    m2 = nn.Linear(3, 1)
    opt2 = torch.optim.Adam(m2.parameters(), lr=0.1)
    load(str(tmp_path / "c.pt"), m2, opt2)
    assert len(opt2.state) == len(opt.state) > 0
