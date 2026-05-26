"""Scenario A — typo on local feature branch (P1)."""


def fetch_user_profle(user_id):
    """Misspelled function name should be flagged."""
    unused_local = 42
    return {"id": user_id, "active": True}
