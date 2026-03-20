"""Input validation utilities with clean patterns."""

from __future__ import annotations

import re
from typing import Optional

_EMAIL_PATTERN = re.compile(
    r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
)
_SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_USERNAME_PATTERN = re.compile(r"^[a-zA-Z][a-zA-Z0-9_]{2,29}$")


def validate_email(email: str) -> Optional[str]:
    """Validate an email address.

    Returns:
        The normalized email if valid, None otherwise.
    """
    if not email or not isinstance(email, str):
        return None

    normalized = email.strip().lower()
    if not _EMAIL_PATTERN.match(normalized):
        return None

    return normalized


def validate_slug(slug: str) -> bool:
    """Check if a string is a valid URL slug."""
    if not slug or not isinstance(slug, str):
        return False
    if len(slug) > 100:
        return False
    return bool(_SLUG_PATTERN.match(slug))


def validate_username(username: str) -> bool:
    """Check if a username meets requirements.

    Rules:
        - Starts with a letter
        - 3-30 characters long
        - Only letters, digits, and underscores
    """
    if not username or not isinstance(username, str):
        return False
    return bool(_USERNAME_PATTERN.match(username))


def validate_port(port: int) -> bool:
    """Check if a port number is in the valid range."""
    return isinstance(port, int) and 1 <= port <= 65535


def validate_pagination(
    page: int,
    page_size: int,
    max_page_size: int = 100,
) -> tuple[int, int]:
    """Normalize and validate pagination parameters.

    Returns:
        A tuple of (page, page_size) clamped to valid ranges.
    """
    safe_page = max(1, page) if isinstance(page, int) else 1
    safe_size = (
        min(max(1, page_size), max_page_size)
        if isinstance(page_size, int)
        else 20
    )
    return safe_page, safe_size
