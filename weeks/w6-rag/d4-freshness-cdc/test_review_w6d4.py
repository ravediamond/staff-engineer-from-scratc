from review_w6d4 import Index


def test_review_older_does_not_overwrite():
    i = Index()
    i.upsert("proc", 7, "current procedure")
    i.upsert("proc", 3, "backfilled old procedure")
    assert i.docs["proc"] == (7, "current procedure")
