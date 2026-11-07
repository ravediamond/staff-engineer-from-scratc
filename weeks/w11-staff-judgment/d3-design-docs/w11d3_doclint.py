"""W11 D3: a linter for design docs (RFCs)."""
import re

REQUIRED = ["context", "goals", "non-goals", "proposal", "alternatives considered", "risks", "rollout", "metrics"]


def strip_code_blocks(md: str) -> str:
    """Remove fenced code blocks (``` ... ```), fences included."""
    # TODO
    raise NotImplementedError


def sections(md: str) -> dict:
    """{lowercased '## ' heading title: body text until the next '## ' heading}, ignoring code blocks.
    '### ' subheadings stay inside the body."""
    # TODO
    raise NotImplementedError


def count_alternatives(body: str) -> int:
    """Number of '### ' subheadings if any, else number of top-level bullet lines ('- ' or '* ' at line start).
    Options named 'do nothing' or 'status quo' (case-insensitive) do not count."""
    # TODO
    raise NotImplementedError


def lint(md: str) -> list:
    """Issues, in this order:
      f"missing section: {name}" for each REQUIRED name absent (in REQUIRED order)
      "non-goals is empty"                         if present but empty
      "need at least 2 alternatives"               if present with fewer than 2 real alternatives
      "metrics need numbers"                       if present without any digit
    """
    # TODO
    raise NotImplementedError
