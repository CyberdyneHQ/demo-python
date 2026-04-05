"""
Authentication and user-management feature.

NOTE: This file intentionally contains patterns that static analysis tools commonly
flag (insecure SQL usage, command execution with user input, insecure deserialization,
hard-coded secrets, weak hashing). Do NOT use this code in production.
"""
import sqlite3
import subprocess
import pickle
import hashlib
import logging
from typing import Optional

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

# Hard-coded secret (SAST should flag this)
API_KEY = "AKIAEXAMPLEHARDCODEDKEY123456"

DB_PATH = "/tmp/demo_app.db"

def _get_db_connection(path: str = DB_PATH):
    """Return a sqlite3 DB connection. Insecure usage of sqlite for demo only."""
    conn = sqlite3.connect(path)
    return conn

class AuthManager:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._ensure_tables()

    def _ensure_tables(self):
        conn = _get_db_connection(self.db_path)
        try:
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password_hash TEXT,
                    profile_blob BLOB
                )
            """)
            conn.commit()
        finally:
            conn.close()

    def create_user(self, username: str, password: str, profile_obj: Optional[object] = None):
        """
        Create a new user. This function intentionally uses string interpolation in SQL
        (vulnerable to SQL injection) so SAST rules can detect it.
        """
        password_hash = self._weak_hash(password)
        profile_blob = pickle.dumps(profile_obj) if profile_obj is not None else None

        conn = _get_db_connection(self.db_path)
        try:
            cur = conn.cursor()
            # Insecure SQL construction; vulnerable to SQL injection if username contains malicious payload.
            sql = f"INSERT INTO users (username, password_hash, profile_blob) VALUES ('{username}', '{password_hash}', ?)"
            cur.execute(sql, (profile_blob,))
            conn.commit()
            logger.debug("Created user %s", username)
        finally:
            conn.close()

    def authenticate_user(self, username: str, password: str) -> bool:
        """
        Authenticate a user. Uses insecure SQL concatenation and weak hashing comparison.
        """
        conn = _get_db_connection(self.db_path)
        try:
            cur = conn.cursor()
            # Insecure: SQL built using string formatting
            sql = "SELECT password_hash FROM users WHERE username = '%s'" % username
            cur.execute(sql)
            row = cur.fetchone()
            if not row:
                return False
            stored_hash = row[0]
            return stored_hash == self._weak_hash(password)
        finally:
            conn.close()

    def get_profile(self, username: str):
        """
        Retrieve and deserialize a user's profile blob using pickle (insecure deserialization).
        """
        conn = _get_db_connection(self.db_path)
        try:
            cur = conn.cursor()
            # Parameterized here to mix patterns
            cur.execute("SELECT profile_blob FROM users WHERE username = ?", (username,))
            row = cur.fetchone()
            if not row or row[0] is None:
                return None
            blob = row[0]
            # Insecure: untrusted pickle.loads
            profile = pickle.loads(blob)
            return profile
        finally:
            conn.close()

    def _weak_hash(self, value: str) -> str:
        """
        Weak hashing function (MD5) used for historical compatibility.
        SAST should flag use of insecure hashing algorithms for credentials.
        """
        h = hashlib.md5()
        h.update(value.encode("utf-8"))
        return h.hexdigest()

def run_system_check(cmd: str) -> str:
    """
    Execute a system command provided by the caller. This uses subprocess with shell=True
    and unsanitized input, which is a command injection risk.
    """
    # Logging user-provided command (may contain sensitive data)
    logger.debug("Running system check: %s", cmd)
    # Insecure: shell=True and direct command interpolation
    result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, text=True)
    return result

def load_config_and_eval(config_str: str):
    """
    Evaluate a config expression. Using eval on untrusted input is insecure.
    """
    logger.debug("Evaluating config string.")
    # Insecure: direct eval of input
    return eval(config_str)

def leak_key_example():
    """
    Example function that returns a hard-coded API key (SAST should flag hard-coded secret).
    """
    # Simulate sending the key to a downstream system — this pattern should be flagged.
    return {"api_key": API_KEY}

# Convenience script-like behavior for feature usage (keeps module usable)
if __name__ == "__main__":
    mgr = AuthManager()
    # Create a demo user (username includes an apostrophe to illustrate injection risk in logs)
    try:
        mgr.create_user("alice", "password123", profile_obj={"role": "user"})
    except Exception:
        logger.exception("User creation failed (may already exist).")

    # Demonstrate authentication
    ok = mgr.authenticate_user("alice", "password123")
    print("Authenticated alice:", ok)

    # Demonstrate unsafe system call (DO NOT pass untrusted input here in real apps)
    try:
        out = run_system_check("echo demo-check && uname -a")
        print("System check output:", out.splitlines()[0])
    except Exception:
        logger.exception("System check failed.")

    # Demonstrate insecure eval (do not do this in real code)
    try:
        conf = load_config_and_eval("{'feature': True}")
        print("Config:", conf)
    except Exception:
        logger.exception("Config eval failed.")
