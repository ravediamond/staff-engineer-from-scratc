"""Review: checkpoint discovery on restart. After a node failure during a save, the job restarted and
crashed with 'file not found' in a loop. Find the bug, fix it, explain:

WHY:
"""
import json
import os


def latest(root):
    steps = sorted((int(d.split("-")[1]) for d in os.listdir(root) if d.startswith("step-")), reverse=True)
    for s in steps:
        d = os.path.join(root, f"step-{s:06d}")
        mpath = os.path.join(d, "manifest.json")
        if not os.path.exists(mpath):
            continue
        return s
    return None
