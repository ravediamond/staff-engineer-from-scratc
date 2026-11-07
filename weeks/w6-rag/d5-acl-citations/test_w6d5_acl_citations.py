import random

import pytest

from w6d5_acl_citations import acl_topk, query_cost, should_abstain, support_score, unsupported_sentences


def test_acl_prefilter_returns_k():
    rng = random.Random(0)
    scores = {f"c{i}": rng.random() for i in range(1000)}
    acl = {c: ({"maintenance"} if i % 50 == 0 else {"finance"}) for i, c in enumerate(scores)}
    got = acl_topk(scores, acl, {"maintenance"}, 10)
    assert len(got) == 10
    assert all("maintenance" in acl[c] for c in got)
    allowed_sorted = sorted((c for c in scores if "maintenance" in acl[c]), key=lambda c: -scores[c])
    assert got == allowed_sorted[:10]


def test_acl_missing_means_nobody():
    assert acl_topk({"a": 1.0, "b": 0.5}, {"b": {"x"}}, {"x"}, 5) == ["b"]


def test_support_score():
    chunk = "Replace the pump seal every 500 operating hours."
    assert support_score("Replace the seal every 500 hours.", [chunk]) == pytest.approx(1.0)
    assert support_score("Replace the seal every 1000 hours.", [chunk]) == pytest.approx(3 / 4)
    assert support_score("the and of", [chunk]) == 1.0


def test_unsupported_sentences():
    chunks = {"c1": "Replace the pump seal every 500 operating hours.", "c2": "Lock out the motor first."}
    answer = [
        {"text": "Lock out the motor first.", "cites": ["c2"]},
        {"text": "Replace the seal every 500 hours.", "cites": ["c1"]},
        {"text": "Also lubricate the coupling monthly.", "cites": ["c1"]},
        {"text": "Call the vendor.", "cites": []},
        {"text": "Seal every 500 hours.", "cites": ["c9"]},
    ]
    assert unsupported_sentences(answer, chunks, threshold=0.8) == [2, 3, 4]


def test_abstain_and_cost():
    assert should_abstain([], 0.5) and should_abstain([0.2, 0.4], 0.5) and not should_abstain([0.6], 0.5)
    assert query_cost(3000, 300, 3, 15, embed_tokens=20, usd_per_m_embed=0.1) == pytest.approx(0.013502)
