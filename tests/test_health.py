"""Contract tests for the minimal, non-sensitive health endpoint and settings."""

import os
import subprocess
import sys

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


class SettingsFailClosedTests(SimpleTestCase):
    def assert_settings_import_fails(self, *, secret_key, allowed_hosts, message):
        environment = os.environ.copy()
        environment.pop("DJANGO_SECRET_KEY", None)
        environment.pop("DJANGO_ALLOWED_HOSTS", None)

        if secret_key is not None:
            environment["DJANGO_SECRET_KEY"] = secret_key
        if allowed_hosts is not None:
            environment["DJANGO_ALLOWED_HOSTS"] = allowed_hosts

        result = subprocess.run(
            [sys.executable, "-c", "import config.settings"],
            capture_output=True,
            check=False,
            env=environment,
            text=True,
            timeout=10,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn(message, result.stderr)

    def test_missing_secret_key_fails_closed(self):
        self.assert_settings_import_fails(
            secret_key=None,
            allowed_hosts="localhost",
            message="DJANGO_SECRET_KEY must be set",
        )

    def test_empty_allowed_hosts_fails_closed(self):
        self.assert_settings_import_fails(
            secret_key="test-only-secret-not-for-production",
            allowed_hosts="",
            message="DJANGO_ALLOWED_HOSTS must contain explicit hostnames",
        )

    def test_wildcard_allowed_hosts_fails_closed(self):
        self.assert_settings_import_fails(
            secret_key="test-only-secret-not-for-production",
            allowed_hosts="*",
            message="DJANGO_ALLOWED_HOSTS must contain explicit hostnames",
        )
