from review_w13d2 import Leader


def test_review_consumers_only_see_replicated_records():
    lead = Leader({"f1", "f2"})
    lead.append("pay-1")
    lead.append("pay-2")
    assert lead.consumer_read(0) == [], "nothing is on the followers yet"
    lead.on_fetch("f1", 2)
    assert lead.consumer_read(0) == []
    lead.on_fetch("f2", 1)
    assert lead.consumer_read(0) == ["pay-1"]
