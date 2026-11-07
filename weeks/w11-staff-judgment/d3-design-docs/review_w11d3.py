"""Review: the doc-lint bot passed an RFC that had no Rollout section at all (the only 'Rollout' was inside a code
example). Find the bug, fix it, explain:

WHY:
"""
import re


def has_section(md, name):
    text = md
    return re.search(rf"^## {re.escape(name)}\s*$", text, flags=re.M | re.I) is not None
