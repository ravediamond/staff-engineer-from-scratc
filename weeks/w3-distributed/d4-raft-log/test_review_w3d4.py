from review_w3d4 import advance_commit


def test_review_no_counting_old_terms():
    log = [(1, "a"), (2, "b")]
    assert advance_commit(log, current_term=4, commit_index=1, match_indexes=[2, 2, 0, 0]) == 1
    log.append((4, "c"))
    assert advance_commit(log, current_term=4, commit_index=1, match_indexes=[3, 3, 0, 0]) == 3
