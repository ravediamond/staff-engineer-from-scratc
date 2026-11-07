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
    # TODO
    raise NotImplementedError


def coverage(stories: list, axes: list) -> dict:
    """{axis: sorted ids of VALID stories tagged with it} for each axis."""
    # TODO
    raise NotImplementedError


def gaps(cov: dict, min_stories: int = 2) -> list:
    """Axes (in cov order) with fewer than min_stories stories."""
    # TODO
    raise NotImplementedError


def pick_story(stories: list, wanted: list):
    """Valid story with the most signals in `wanted`; ties -> more digits in result; then lower id. None if no overlap."""
    # TODO
    raise NotImplementedError
