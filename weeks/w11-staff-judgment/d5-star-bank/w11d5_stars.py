"""W11 D5: STAR stories as data: validation, coverage, gaps, retrieval."""
import re

REQUIRED_FIELDS = ["id", "title", "situation", "task", "action", "result", "signals"]
STAFF_SIGNALS = ["scope", "ambiguity", "influence", "technical-depth", "execution", "people-growth", "conflict"]


def validate_story(s: dict) -> list:
    """Issues, in order:
      f"missing {field}" for each REQUIRED_FIELDS entry absent or empty (in order)
      "result needs a number"            if result present and has no digit
      "action too short"                 if action present with fewer than 25 words
      f"unknown signal {x}"              for each signal not in STAFF_SIGNALS (in story order)
    """
    issues = [f"missing {f}" for f in REQUIRED_FIELDS if not s.get(f)]
    if s.get("result") and not re.search(r"\d", s["result"]):
        issues.append("result needs a number")
    if s.get("action") and len(s["action"].split()) < 25:
        issues.append("action too short")
    for x in s.get("signals") or []:
        if x not in STAFF_SIGNALS:
            issues.append(f"unknown signal {x}")
    return issues


def coverage(stories: list, axes: list) -> dict:
    """{axis: sorted ids of VALID stories tagged with it} for each axis."""
    valid = [s for s in stories if not validate_story(s)]
    return {a: sorted(s["id"] for s in valid if a in s["signals"]) for a in axes}


def gaps(cov: dict, min_stories: int = 2) -> list:
    """Axes (in cov order) with fewer than min_stories stories."""
    return [a for a, ids in cov.items() if len(ids) < min_stories]


def pick_story(stories: list, wanted: list):
    """Valid story with the most signals in `wanted`; ties -> more digits in result; then lower id. None if no overlap."""
    best, best_key = None, None
    for s in stories:
        if validate_story(s):
            continue
        overlap = len(set(s["signals"]) & set(wanted))
        if overlap == 0:
            continue
        key = (-overlap, -len(re.findall(r"\d", s["result"])), s["id"])
        if best_key is None or key < best_key:
            best, best_key = s, key
    return best
