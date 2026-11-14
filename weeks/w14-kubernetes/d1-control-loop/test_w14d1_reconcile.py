from w14d1_reconcile import Store, WorkQueue, reconcile_replicaset


def owned(store, name="web"):
    return [p for p in store.list("Pod") if p["owner"] == name]


def test_work_queue_deduplicates():
    q = WorkQueue()
    for key in ["rs/web", "rs/api", "rs/web", "rs/web"]:
        q.add(key)
    assert len(q) == 2
    assert q.get() == "rs/web"
    q.add("rs/web")
    assert [q.get(), q.get(), q.get()] == ["rs/api", "rs/web", None]


def test_creates_to_match_and_is_idempotent():
    s = Store()
    s.create("ReplicaSet", "web", replicas=3)
    out = reconcile_replicaset(s, "web")
    assert len(out["created"]) == 3 and len(owned(s)) == 3
    assert len({p["name"] for p in owned(s)}) == 3
    assert reconcile_replicaset(s, "web") == {"created": [], "deleted": []}


def test_level_triggered_heals_without_events():
    s = Store()
    s.create("ReplicaSet", "web", replicas=3)
    s.create("ReplicaSet", "api", replicas=1)
    reconcile_replicaset(s, "web")
    reconcile_replicaset(s, "api")
    victim = owned(s)[0]["name"]
    del s.objects[("Pod", victim)]            # deleted behind the controller's back: no event at all
    s.events.clear()
    out = reconcile_replicaset(s, "web")
    assert len(out["created"]) == 1 and len(owned(s)) == 3
    assert len(owned(s, "api")) == 1, "only pods owned by this ReplicaSet are touched"


def test_scale_down_removes_unready_then_newest():
    s = Store()
    s.create("ReplicaSet", "web", replicas=5)
    reconcile_replicaset(s, "web")
    pods = owned(s)
    for p in pods[:4]:
        s.update("Pod", p["name"], ready=True)
    s.update("ReplicaSet", "web", replicas=3)
    out = reconcile_replicaset(s, "web")
    newest_ready = max(pods[:4], key=lambda p: p["created"])["name"]
    assert set(out["deleted"]) == {pods[4]["name"], newest_ready}
    assert len(owned(s)) == 3 and all(p["ready"] for p in owned(s))


def test_deleted_replicaset_garbage_collects_pods():
    s = Store()
    s.create("ReplicaSet", "web", replicas=2)
    reconcile_replicaset(s, "web")
    s.delete("ReplicaSet", "web")
    out = reconcile_replicaset(s, "web")
    assert len(out["deleted"]) == 2 and owned(s) == []
