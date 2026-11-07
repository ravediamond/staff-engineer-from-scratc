import json
import os

from review_w9d5 import latest


def make(root, step, shards, present):
    d = os.path.join(root, f"step-{step:06d}")
    os.makedirs(d)
    with open(os.path.join(d, "manifest.json"), "w") as f:
        json.dump({"step": step, "shards": {s: "x" for s in shards}}, f)
    for s in present:
        open(os.path.join(d, s), "w").close()


def test_review_manifest_with_missing_shard(tmp_path):
    root = str(tmp_path)
    make(root, 10, ["a", "b"], ["a", "b"])
    make(root, 20, ["a", "b"], ["a"])
    assert latest(root) == 10
