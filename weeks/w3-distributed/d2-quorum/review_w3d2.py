"""Review: quorum read path. Users intermittently see their old profile right after saving.
Writes use W=2 of N=3 and reads R=2. Find the bug, fix it, explain:

WHY:
"""


def quorum_read(replicas, key, r):
    """replicas: list of dicts {key: (version, value)}. Ask the first r replicas that have answered."""
    responses = [rep[key] for rep in replicas[:r] if key in rep]
    if not responses:
        return None
    return max(responses, key=lambda vv: vv[0])[1]
