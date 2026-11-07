"""Review: a BM25 scorer copied from a blog. Long, rambling documents keep winning the search.
Find the bug, fix it, explain:

WHY:
"""
import math


def bm25_term(tf, df, n_docs, doc_len, avgdl, k1=1.5, b=0.75):
    idf = math.log((n_docs - df + 0.5) / (df + 0.5) + 1)
    norm = k1 * (1 - b + b * doc_len / avgdl)
    return idf * tf * (k1 + 1) / (tf + norm)
