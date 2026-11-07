import numpy as np
import pytest

from w6d2_hybrid import HybridIndex, hash_embed, minmax_fuse, rrf


def test_hash_embed_deterministic_normalised():
    a, b = hash_embed("pump seal leak"), hash_embed("pump seal leak")
    assert np.allclose(a, b) and abs(np.linalg.norm(a) - 1) < 1e-9
    assert hash_embed("").sum() == 0
    assert a @ hash_embed("seal leak on the pump") > a @ hash_embed("quarterly revenue report")


def test_rrf_formula_and_order():
    out = rrf([["a", "b", "c"], ["b", "c", "d"]], k=60)
    assert out[0] == "b"
    assert out.index("c") < out.index("a")
    assert rrf([["x"], ["y"]], k=60) == ["x", "y"], "tie broken by id"


def test_rrf_exact_value():
    from collections import defaultdict
    ranks = [["a", "b"], ["b"]]
    out = rrf(ranks, k=1)
    assert out == ["b", "a"]  # b: 1/3 + 1/2 > a: 1/2


def test_minmax_fuse():
    f = minmax_fuse([{"a": 10, "b": 5, "c": 0}, {"b": 0.9, "d": 0.1}], [0.5, 0.5])
    assert f["a"] == pytest.approx(0.5) and f["b"] == pytest.approx(0.75)
    assert f["c"] == 0 and f["d"] == pytest.approx(0)
    assert minmax_fuse([{"x": 3, "y": 3}], [1.0]) == {"x": 1.0, "y": 1.0}


def test_hybrid_modes():
    docs = {
        "d1": "Error E4471 indicates a seal leak on pump P101",
        "d2": "How to replace a leaking seal on a centrifugal pump",
        "d3": "Compressor condensate drain schedule",
        "d4": "Seal leak troubleshooting guide for pumps and compressors",
    }
    idx = HybridIndex(docs)
    assert idx.search("E4471", 1, "bm25") == ["d1"]
    fused = idx.search("pump seal leak E4471", 3, "rrf")
    assert fused[0] == "d1" and len(fused) == 3
    assert set(idx.search("seal leak", 2, "dense")) == {"d1", "d4"}, "both contain the bigram 'seal leak'"
    assert "d3" not in idx.search("seal leak", 3, "dense")
