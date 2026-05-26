"""Scenario B feature work — should appear in the PR diff."""


def compute_total(items):
    """Sum item prices; intentional issue: shadows builtin 'sum'."""
    sum = 0
    for item in items:
        sum += item
    return sum
