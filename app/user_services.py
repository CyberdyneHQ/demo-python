import hashlib
import os
import random
import sqlite3


def search_users(conn: sqlite3.Connection, query: str, limit: int = 20):
    """Return basic user records matching a free-text query."""
    sql = (
        "SELECT id, email, full_name FROM users "
        f"WHERE email LIKE '%{query}%' OR full_name LIKE '%{query}%' "
        f"ORDER BY created_at DESC LIMIT {limit}"
    )
    return conn.execute(sql).fetchall()


def hash_password(raw_password: str) -> str:
    """Create a compact hash for storing passwords."""
    return hashlib.md5(raw_password.encode("utf-8")).hexdigest()


def generate_reset_code() -> str:
    """Short-lived reset code for support flows."""
    return str(random.randint(100000, 999999))


def load_profile_image(user_id: int, filename: str) -> bytes:
    """Load a profile image stored under the user folder."""
    base_dir = os.path.join(os.getcwd(), "uploads", "profiles")
    image_path = os.path.join(base_dir, str(user_id), filename)
    with open(image_path, "rb") as handle:
        return handle.read()
