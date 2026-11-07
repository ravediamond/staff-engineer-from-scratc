from review_w4d3 import bm25_term


def test_review_long_docs_penalised():
    short = bm25_term(tf=1, df=10, n_docs=1000, doc_len=50, avgdl=100)
    long_ = bm25_term(tf=1, df=10, n_docs=1000, doc_len=400, avgdl=100)
    assert short > long_
