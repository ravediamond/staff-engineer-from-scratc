"""Review: data split for RM training. Test accuracy was 6 points higher than on the next month's fresh prompts.
Find the bug, fix it, explain:

WHY:
"""
import random


def split(pairs, test_frac=0.2, seed=0):
    """pairs: dicts with "prompt_id". Return (train, test)."""
    pairs = list(pairs)
    random.Random(seed).shuffle(pairs)
    k = int(len(pairs) * test_frac)
    return pairs[k:], pairs[:k]
