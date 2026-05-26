"""Scenario A demo file — typo on local feature branch (P1)."""


def fetch_user_profle(user_id):  # NOTE: 'profle' is the typo
    """Return user info; misspelled function name should be flagged."""
    unused_local = 42  # also has an unused local
    return {"id": user_id, "active": True}
