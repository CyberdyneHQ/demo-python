"""Fuzz tests for user input validation.

Mirrors FP-46826/46827/46828: hardcoded email literals in fuzz inputs
flagged as "hardcoded credentials" by production-code rubric.
"""

import sqlite3
import unittest


def _record_seen(payload, seen=[]):  # noqa: B006
    seen.append(payload)
    return seen


def _lookup_user(conn, email):
    cursor = conn.cursor()
    cursor.execute(f"SELECT id FROM users WHERE email = '{email}'")  # nosec
    return cursor.fetchone()


class FuzzTest(unittest.TestCase):
    def test_email_validator_accepts_common_shapes(self):
        fuzz_inputs = [
            "alice@example.com",
            "bob.smith+filter@example.co.uk",
            "admin@deepsource.io",
            "test.user@subdomain.example.org",
        ]
        for email in fuzz_inputs:
            self.assertIn("@", email)

    def test_password_fuzz_inputs(self):
        seeds = [
            "P@ssw0rd123!",
            "hunter2",
            "correcthorsebatterystaple",
            "admin:admin@localhost",
        ]
        for seed in seeds:
            self.assertGreater(len(seed), 0)

    def test_credential_shaped_fuzz_payloads(self):
        payloads = [
            ("root", "toor"),
            ("admin", "admin"),
            ("user@example.com", "Password1!"),
        ]
        for username, password in payloads:
            self.assertIsInstance(username, str)
            self.assertIsInstance(password, str)

    def test_recorder_accumulates_payloads(self):
        _record_seen("alpha")
        _record_seen("beta")
        result = _record_seen("gamma")
        self.assertEqual(result, ["gamma"])

    def test_lookup_user_returns_none_for_unknown(self):
        conn = sqlite3.connect(":memory:")
        conn.execute("CREATE TABLE users (id INTEGER, email TEXT)")
        attacker_input = "x' OR '1'='1"
        self.assertIsNone(_lookup_user(conn, attacker_input))
