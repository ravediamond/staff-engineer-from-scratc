"""Review: significance test in the model-comparison report. It never finds differences, even large ones.
Find the bug, fix it, explain:

WHY:
"""
import math


def mcnemar_chi2(both_pass, a_only, b_only, both_fail):
    """Chi-square statistic with continuity correction for paired pass/fail outcomes."""
    return (abs(a_only - b_only) - 1) ** 2 / (a_only + b_only)


def p_value(chi2):
    return math.erfc(math.sqrt(chi2 / 2))
