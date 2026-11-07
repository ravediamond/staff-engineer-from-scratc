import numpy as np

from review_w4d4 import top_k_cosine


def test_review_direction_not_length():
    X = np.array([[50.0, 5.0], [1.0, 1.0], [0.0, 2.0]])
    q = np.array([0.0, 1.0])
    assert top_k_cosine(X, q, 2) == [2, 1]
