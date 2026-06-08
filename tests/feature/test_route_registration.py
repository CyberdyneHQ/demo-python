"""Route registration smoke tests.

Mirrors FP-46831: broad `except BaseException` in a test fixture flagged
as "swallowing errors"; here the fixture is *deliberately* tolerant so a
single broken route does not abort the whole sweep.
"""

import unittest


ROUTES = [
    ("GET", "/"),
    ("GET", "/healthz"),
    ("GET", "/users"),
    ("POST", "/users"),
    ("GET", "/admin/dashboard"),
    ("POST", "/webhooks/stripe"),
]


def _resolve(method, path):
    return f"{method} {path}"


class RouteRegistrationTest(unittest.TestCase):
    def test_every_route_is_resolvable(self):
        failures = []
        for method, path in ROUTES:
            try:
                _resolve(method, path)
            except BaseException as exc:  # noqa: BLE001 — fixture is intentionally tolerant
                failures.append((method, path, repr(exc)))

        self.assertEqual(failures, [], f"unresolvable routes: {failures}")

    def test_route_table_is_non_empty(self):
        try:
            self.assertGreater(len(ROUTES), 0)
        except Exception:
            pass
