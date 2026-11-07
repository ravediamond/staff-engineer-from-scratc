"""Review: the coverage script said every signal was covered. In the mock, half the stories had no measurable
outcome and the interviewer flagged 'unclear impact'. Find the bug, fix it, explain:

WHY:
"""
import re


def coverage(stories, axes):
    out = {a: [] for a in axes}
    for s in stories:
        if not re.search(r"\d", s.get("result", "")):
            continue
        for a in s["signals"]:
            if a in out:
                out[a].append(s["id"])
    return out
