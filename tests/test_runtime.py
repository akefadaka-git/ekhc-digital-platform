"""Regression tests for runtime secret and host configuration validation."""

from django.core.exceptions import ImproperlyConfigured
from django.test import SimpleTestCase

from config.runtime import load_runtime_settings, parse_allowed_hosts


class AllowedHostParsingTests(SimpleTestCase):
    def test_accepts_explicit_domains_ips_and_subdomain_patterns(self):
        self.assertEqual(
            parse_allowed_hosts("localhost,127.0.0.1,.example.org,api.example.org"),
            ["localhost", "127.0.0.1", ".example.org", "api.example.org"],
        )

    def test_rejects_wildcard_hosts(self):
        for value in ("*", "*.example.org", "api.*.example.org"):
            with self.subTest(value=value):
                with self.assertRaisesMessage(
                    ImproperlyConfigured, "invalid host entry"
                ):
                    parse_allowed_hosts(value)

    def test_rejects_empty_entries(self):
        for value in ("example.org,", ",example.org", "example.org,,api.example.org"):
            with self.subTest(value=value):
                with self.assertRaisesMessage(
                    ImproperlyConfigured, "empty entries"
                ):
                    parse_allowed_hosts(value)

    def test_rejects_urls_ports_paths_and_whitespace(self):
        for value in (
            "https://example.org",
            "example.org:8443",
            "example.org/admin",
            "bad host.example.org",
        ):
            with self.subTest(value=value):
                with self.assertRaisesMessage(
                    ImproperlyConfigured, "invalid host entry"
                ):
                    parse_allowed_hosts(value)

    def test_rejects_duplicate_hosts_case_insensitively(self):
        with self.assertRaisesMessage(ImproperlyConfigured, "duplicate entries"):
            parse_allowed_hosts("Example.org,example.org")


class RuntimeSecretTests(SimpleTestCase):
    def test_secret_is_required_without_echoing_value(self):
        with self.assertRaisesMessage(
            ImproperlyConfigured, "DJANGO_SECRET_KEY must be set"
        ):
            load_runtime_settings(
                {"DJANGO_SECRET_KEY": "", "DJANGO_ALLOWED_HOSTS": "localhost"},
                "development",
            )

    def test_development_keeps_existing_local_secret_compatibility(self):
        result = load_runtime_settings(
            {
                "DJANGO_SECRET_KEY": "local-development-key",
                "DJANGO_ALLOWED_HOSTS": "localhost",
            },
            "development",
        )
        self.assertEqual(result["secret_key"], "local-development-key")
        self.assertEqual(result["allowed_hosts"], ["localhost"])

    def test_production_rejects_short_secret(self):
        with self.assertRaisesMessage(
            ImproperlyConfigured, "at least 50 non-whitespace characters"
        ):
            load_runtime_settings(
                {
                    "DJANGO_SECRET_KEY": "short",
                    "DJANGO_ALLOWED_HOSTS": "example.org",
                },
                "production",
            )

    def test_production_rejects_known_placeholder_secret(self):
        with self.assertRaisesMessage(
            ImproperlyConfigured, "non-placeholder value"
        ):
            load_runtime_settings(
                {
                    "DJANGO_SECRET_KEY": "not-for-production-" + "x" * 50,
                    "DJANGO_ALLOWED_HOSTS": "example.org",
                },
                "production",
            )

    def test_production_rejects_whitespace_in_secret(self):
        with self.assertRaisesMessage(
            ImproperlyConfigured, "non-placeholder value"
        ):
            load_runtime_settings(
                {
                    "DJANGO_SECRET_KEY": "a" * 25 + " " + "b" * 25,
                    "DJANGO_ALLOWED_HOSTS": "example.org",
                },
                "production",
            )

    def test_production_accepts_long_non_placeholder_secret(self):
        result = load_runtime_settings(
            {
                "DJANGO_SECRET_KEY": "a9!b8@c7#d6$e5%f4^g3&h2*j1(k0)_l9+m8=n7",
                "DJANGO_ALLOWED_HOSTS": "example.org",
            },
            "production",
        )
        self.assertEqual(result["allowed_hosts"], ["example.org"])
