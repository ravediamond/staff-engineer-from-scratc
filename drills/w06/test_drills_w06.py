from d21_word_search import exist
from d22_cheapest_flights import cheapest
from d23_accounts_merge import accounts_merge
from d24_alien_dictionary import alien_order

BOARD = [["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]]


def test_d21():
    assert exist([r[:] for r in BOARD], "ABCCED")
    assert exist([r[:] for r in BOARD], "SEE")
    assert not exist([r[:] for r in BOARD], "ABCB")


def test_d22():
    fl = [(0, 1, 100), (1, 2, 100), (2, 0, 100), (1, 3, 600), (2, 3, 200)]
    assert cheapest(4, fl, 0, 3, 1) == 700
    assert cheapest(4, fl, 0, 3, 2) == 400
    assert cheapest(3, [(0, 1, 100), (1, 2, 100), (0, 2, 500)], 0, 2, 0) == 500
    assert cheapest(3, [(0, 1, 1)], 0, 2, 5) == -1


def test_d23():
    acc = [["John", "johnsmith@mail.com", "john_newyork@mail.com"], ["John", "johnsmith@mail.com", "john00@mail.com"],
           ["Mary", "mary@mail.com"], ["John", "johnnybravo@mail.com"]]
    assert accounts_merge(acc) == [["John", "john00@mail.com", "john_newyork@mail.com", "johnsmith@mail.com"],
                                   ["John", "johnnybravo@mail.com"], ["Mary", "mary@mail.com"]]


def test_d24():
    assert alien_order(["wrt", "wrf", "er", "ett", "rftt"]) == "wertf"
    assert alien_order(["z", "x"]) == "zx"
    assert alien_order(["z", "x", "z"]) == ""
    assert alien_order(["abc", "ab"]) == ""
    assert alien_order(["ab", "adc"]) == "abcd"
