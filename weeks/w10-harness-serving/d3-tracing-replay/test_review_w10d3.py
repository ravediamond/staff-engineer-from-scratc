import pytest

from review_w10d3 import Replay


def test_review_per_call_matching():
    rec = [{"tool": "search", "args": {"q": "a"}, "output": "A"},
           {"tool": "search", "args": {"q": "b"}, "output": "B"}]
    r = Replay(rec)
    assert r.call("search", q="a") == "A"
    assert r.call("search", q="b") == "B"
    with pytest.raises(KeyError):
        Replay(rec).call("search", q="zzz")
