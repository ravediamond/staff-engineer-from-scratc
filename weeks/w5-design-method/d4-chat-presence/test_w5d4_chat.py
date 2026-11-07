from w5d4_chat import ChatService, Presence


def test_seq_and_idempotent_send():
    c = ChatService()
    assert c.send("g", "ana", "m1", "hi") == 1
    assert c.send("g", "bo", "m2", "yo") == 2
    assert c.send("g", "ana", "m1", "hi") == 1, "retry returns the same seq"
    assert c.send("other", "ana", "m1", "new conv") == 1
    assert [m[0] for m in c.fetch("g")] == [1, 2]


def test_fetch_after_and_limit():
    c = ChatService()
    for i in range(10):
        c.send("g", "u", f"id{i}", str(i))
    assert [m[0] for m in c.fetch("g", after_seq=7)] == [8, 9, 10]
    assert [m[0] for m in c.fetch("g", after_seq=0, limit=3)] == [1, 2, 3]


def test_read_pointer_monotonic_and_unread():
    c = ChatService()
    for i in range(10):
        c.send("g", "bo", f"id{i}", str(i))
    assert c.unread("ana", "g") == 10 and c.unread("bo", "g") == 0
    c.mark_read("ana", "g", 5)
    c.mark_read("ana", "g", 9)
    c.mark_read("ana", "g", 7)  # late ack
    assert c.unread("ana", "g") == 1


def test_presence():
    p = Presence(timeout=60)
    p.heartbeat("ana", 100)
    p.heartbeat("bo", 30)
    assert p.is_online("ana", 159) and not p.is_online("ana", 160)
    assert p.online(["ana", "bo", "zed"], 120) == ["ana"]
    p.heartbeat("ana", 90)  # delayed heartbeat must not move last-seen backwards
    assert p.is_online("ana", 159)
