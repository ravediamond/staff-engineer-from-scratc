import math

from w4d3_bm25 import InvertedIndex, tokenize

DOCS = {
    "d1": "The pump failed with error E-4471 after maintenance",
    "d2": "Pump maintenance procedure: check the seal, then the pump bearing",
    "d3": "Compressor maintenance procedure for oxygen plants",
    "d4": "Error codes reference: E-4471 means seal leak on the pump",
    "d5": "A very long document about plants " + "and maintenance schedules " * 30 + "pump",
}


def build():
    idx = InvertedIndex()
    for d, t in DOCS.items():
        idx.add(d, t)
    return idx


def test_tokenize():
    assert tokenize("Error E-4471, Pump!") == ["error", "e", "4471", "pump"]


def test_stats():
    idx = build()
    assert idx.n_docs == 5
    assert idx.df("pump") == 4 and idx.df("4471") == 2 and idx.df("zzz") == 0
    assert abs(idx.avgdl - sum(len(tokenize(t)) for t in DOCS.values()) / 5) < 1e-9
    assert idx.idf("4471") > idx.idf("pump") > 0


def test_bm25_formula_one_doc():
    idx = InvertedIndex()
    idx.add("a", "x y")
    idx.add("b", "y y z z z")
    k1, b = 1.5, 0.75
    avgdl = 3.5
    idf_y = math.log((2 - 2 + 0.5) / (2 + 0.5) + 1)
    expected_b = idf_y * 2 * (k1 + 1) / (2 + k1 * (1 - b + b * 5 / avgdl))
    scores = dict(idx.bm25("y"))
    assert abs(scores["b"] - expected_b) < 1e-9


def test_ranking_rare_terms_and_length():
    idx = build()
    top = [d for d, _ in idx.bm25("error 4471 pump", k=2)]
    assert set(top) == {"d1", "d4"}
    ranked = [d for d, _ in idx.bm25("pump", k=5)]
    assert ranked.index("d5") > ranked.index("d1"), "long doc with one mention ranks below a short one"
    assert idx.bm25("nothing matches") == []


def test_and_search():
    idx = build()
    assert idx.search_and("pump maintenance") == ["d1", "d2", "d5"]
    assert idx.search_and("4471 seal") == ["d4"]
    assert idx.search_and("pump unicorn") == []
