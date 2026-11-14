from w15d4_replication import Cluster, Session


def test_read_your_writes():
    c = Cluster(["r1", "r2"])
    me, other = Session(), Session()
    c.write(me, "bio", "v1")
    c.replicate("r1")
    c.replicate("r2")
    lsn = c.write(me, "bio", "v2")
    assert lsn == 2 and me.last_write_lsn == 2
    assert c.read(me, "bio") == ("v2", "primary"), "no replica has my write yet"
    assert c.read(other, "bio") == ("v1", "r1"), "a session that wrote nothing may read stale data"
    c.replicate("r2")
    assert c.read(me, "bio") == ("v2", "r2")


def test_monotonic_reads():
    c = Cluster(["r1", "r2"])
    writer, reader = Session(), Session()
    c.write(writer, "k", "a")
    c.replicate("r1")
    c.replicate("r2")
    c.write(writer, "k", "b")
    c.replicate("r2")                       # r1 at LSN 1, r2 at LSN 2
    reader.last_seen_lsn = 2                # the reader already saw "b" (for example served by r2 earlier)
    assert c.read(reader, "k") == ("b", "r2"), "never go back to r1 and see 'a' again"
    fresh = Session()
    assert c.read(fresh, "k") == ("a", "r1"), "least advanced replica that qualifies"
    assert fresh.last_seen_lsn == 1
    c.replicate("r1")
    assert c.read(fresh, "k")[0] == "b" and fresh.last_seen_lsn == 2


def test_replicate_never_goes_back():
    c = Cluster(["r1"])
    s = Session()
    for i in range(5):
        c.write(s, "k", i)
    c.replicate("r1", up_to=4)
    c.replicate("r1", up_to=2)
    assert c.applied["r1"] == 4
    c.replicate("r1", up_to=99)
    assert c.applied["r1"] == 5


def test_async_failover_loses_the_unreplicated_tail():
    c = Cluster(["r1", "r2"])
    s = Session()
    for i in range(10):
        c.write(s, "n", i)
    c.replicate("r1", up_to=7)
    c.replicate("r2", up_to=4)
    out = c.failover()
    assert out == {"new_primary": "r1", "lost_writes": 3, "epoch": 2}
    assert len(c.log) == 7 and c.applied == {"r2": 4}
    assert c.read(Session(), "n")[0] in (3, 6)
    assert s.last_write_lsn == 10, "the client still believes write 10 exists: that is the data loss"


def test_sync_replication_loses_nothing():
    c = Cluster(["r1", "r2"], synchronous=True)
    s = Session()
    for i in range(10):
        c.write(s, "n", i)
    assert max(c.applied.values()) == 10 and min(c.applied.values()) == 0
    out = c.failover()
    assert out["lost_writes"] == 0 and len(c.log) == 10
