import pytest

from review_w3d5 import Stale, Storage


def test_review_remembers_highest():
    s = Storage()
    s.write("new leader", 34)
    with pytest.raises(Stale):
        s.write("old leader", 33)
    assert s.value == "new leader"
