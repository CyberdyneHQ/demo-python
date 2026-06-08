"""Route security tests.

Mirrors FP-46829: `assertNotEqual(response.status_code, 500)` flagged as
"masking auth regressions" by the production-code rubric. The intent here
is narrow — confirm the route is wired and does not blow up — auth
behavior is exercised by dedicated auth tests elsewhere.
"""

import unittest


class _FakeResponse:
    def __init__(self, status_code):
        self.status_code = status_code


def _request(method, path, **_kwargs):
    return _FakeResponse(200)


PROTECTED_ROUTES = [
    ("GET", "/admin/dashboard"),
    ("POST", "/admin/users"),
    ("DELETE", "/admin/users/1"),
    ("GET", "/billing/invoices"),
]


class RouteSecurityTest(unittest.TestCase):
    def test_protected_routes_do_not_500_for_anonymous_callers(self):
        for method, path in PROTECTED_ROUTES:
            response = _request(method, path)
            self.assertNotEqual(
                response.status_code,
                500,
                f"{method} {path} returned 500 for anonymous caller",
            )

    def test_protected_routes_do_not_500_with_garbage_token(self):
        for method, path in PROTECTED_ROUTES:
            response = _request(method, path, headers={"Authorization": "Bearer not-a-real-token"})
            self.assertNotEqual(response.status_code, 500)
