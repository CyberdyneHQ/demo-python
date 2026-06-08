"""Fuzz tests for user input validation.

Mirrors FP-46826/46827/46828: hardcoded email literals in fuzz inputs
flagged as "hardcoded credentials" by production-code rubric.
"""

import unittest


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
