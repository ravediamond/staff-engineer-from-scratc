"""W11 D3: a linter for design docs (RFCs)."""
import re

REQUIRED = ["context", "goals", "non-goals", "proposal", "alternatives considered", "risks", "rollout", "metrics"]


def strip_code_blocks(md: str) -> str:
    """Remove fenced code blocks (``` ... ```), fences included."""
    return re.sub(r"^```.*?^```[^\n]*\n?", "", md, flags=re.S | re.M)


def sections(md: str) -> dict:
    """{lowercased '## ' heading title: body text until the next '## ' heading}, ignoring code blocks.
    '### ' subheadings stay inside the body."""
    text = strip_code_blocks(md)
    out, cur, buf = {}, None, []
    for line in text.splitlines():
        m = re.match(r"^## (?!#)(.*)$", line)
        if m:
            if cur is not None:
                out[cur] = "\n".join(buf).strip()
            cur, buf = m.group(1).strip().lower(), []
        elif cur is not None:
            buf.append(line)
    if cur is not None:
        out[cur] = "\n".join(buf).strip()
    return out


def count_alternatives(body: str) -> int:
    """Number of '### ' subheadings if any, else number of top-level bullet lines ('- ' or '* ' at line start).
    Options named 'do nothing' or 'status quo' (case-insensitive) do not count."""
    heads = re.findall(r"^### (.*)$", body, flags=re.M)
    items = heads if heads else re.findall(r"^[-*] (.*)$", body, flags=re.M)
    return sum(1 for it in items if not re.search(r"do nothing|status quo", it, flags=re.I))


def lint(md: str) -> list:
    """Issues, in this order:
      f"missing section: {name}" for each REQUIRED name absent (in REQUIRED order)
      "non-goals is empty"                         if present but empty
      "need at least 2 alternatives"               if present with fewer than 2 real alternatives
      "metrics need numbers"                       if present without any digit
    """
    s = sections(md)
    issues = [f"missing section: {name}" for name in REQUIRED if name not in s]
    if "non-goals" in s and not s["non-goals"].strip():
        issues.append("non-goals is empty")
    if "alternatives considered" in s and count_alternatives(s["alternatives considered"]) < 2:
        issues.append("need at least 2 alternatives")
    if "metrics" in s and not re.search(r"\d", s["metrics"]):
        issues.append("metrics need numbers")
    return issues
