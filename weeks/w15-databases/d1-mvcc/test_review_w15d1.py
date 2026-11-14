from review_w15d1 import visible


def test_review_snapshot_ignores_later_commits():
    committed = {1, 2, 5, 7}
    # reader 6 began when 5 was still running; 7 started later
    assert visible(1, 6, {5}, 6, committed)
    assert visible(6, 6, {5}, 6, committed)
    assert not visible(5, 6, {5}, 6, committed), "in progress at snapshot time"
    assert not visible(7, 6, {5}, 6, committed), "started after the snapshot"
    assert not visible(3, 6, {5}, 6, committed), "never committed"
