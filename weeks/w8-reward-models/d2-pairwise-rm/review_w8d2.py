"""Review: data split for RM training. Test accuracy was 6 points higher than on the next month's fresh prompts.
Find the bug, fix it, explain:

WHY:
"""
import random


def split(pairs, test_frac=0.2, seed=0):
    """pairs: dicts with "prompt_id". Return (train, test)."""
    ids = sorted({p["prompt_id"] for p in pairs})
    random.Random(seed).shuffle(ids)
    test_ids = set(ids[: int(len(ids) * test_frac)])
    return [p for p in pairs if p["prompt_id"] not in test_ids], [p for p in pairs if p["prompt_id"] in test_ids]
