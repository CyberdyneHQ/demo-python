"""Scenario B — feature work that lands first, then merge master in."""


def compute_total(items):
    """Shadows builtin 'sum'."""
    sum = 0
    for item in items:
        sum += item
    return sum
