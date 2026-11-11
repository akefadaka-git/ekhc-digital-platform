"""Contract tests for the minimal, non-sensitive health endpoint."""

from django.test import SimpleTestCase


class HealthEndpointTests(SimpleTestCase):
    def test_health_returns_minimal_status(self):
        response = self.client.get("/health/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertEqual(response["Cache-Control"], "no-store")
        self.assertEqual(response["X-Content-Type-Options"], "nosniff")
        self.assertEqual(response.json(), {"status": "ok"})

    def test_health_does_not_expose_internal_or_sensitive_values(self):
        response = self.client.get("/health/")
        body = response.content.decode("utf-8").lower()

        for forbidden in (
            "secret",
            "database",
            "settings",
            "environment",
            "member",
            "pastoral",
            "governance",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, body)

    def test_health_rejects_non_get_methods(self):
        response = self.client.post("/health/")
        self.assertEqual(response.status_code, 405)
