"""Regression tests for security headers and deployment boundary validation."""

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.test import RequestFactory, SimpleTestCase

from config.security import load_security_settings


class SecurityHeaderTests(SimpleTestCase):
    def test_baseline_security_headers_are_present(self):
        response = self.client.get("/health/")

        self.assertEqual(response["X-Content-Type-Options"], "nosniff")
        self.assertEqual(response["X-Frame-Options"], "DENY")
        self.assertEqual(response["Referrer-Policy"], "same-origin")
        self.assertEqual(response["Cross-Origin-Opener-Policy"], "same-origin")

    def test_hsts_is_not_emitted_for_plain_http_development_requests(self):
        response = self.client.get("/health/")
        self.assertNotIn("Strict-Transport-Security", response)

    def test_forwarded_proxy_headers_are_not_trusted(self):
        request = RequestFactory().get(
            "/health/",
            HTTP_HOST="testserver",
            HTTP_X_FORWARDED_HOST="attacker.invalid",
            HTTP_X_FORWARDED_PROTO="https",
        )

        self.assertIsNone(settings.SECURE_PROXY_SSL_HEADER)
        self.assertFalse(settings.USE_X_FORWARDED_HOST)
        self.assertFalse(request.is_secure())
        self.assertEqual(request.get_host(), "testserver")


class SecurityConfigurationTests(SimpleTestCase):
    def test_development_defaults_do_not_assume_https_or_proxy_topology(self):
        config = load_security_settings({})

        self.assertEqual(config["environment"], "development")
        self.assertFalse(config["ssl_redirect"])
        self.assertEqual(config["hsts_seconds"], 0)
        self.assertFalse(config["hsts_include_subdomains"])
        self.assertFalse(config["session_cookie_secure"])
        self.assertFalse(config["csrf_cookie_secure"])

    def test_invalid_boolean_fails_closed(self):
        with self.assertRaisesMessage(
            ImproperlyConfigured, "DJANGO_SECURE_SSL_REDIRECT must be exactly"
        ):
            load_security_settings({"DJANGO_SECURE_SSL_REDIRECT": "sometimes"})

    def test_invalid_hsts_duration_fails_closed(self):
        with self.assertRaisesMessage(
            ImproperlyConfigured, "DJANGO_SECURE_HSTS_SECONDS must be a whole number"
        ):
            load_security_settings({"DJANGO_SECURE_HSTS_SECONDS": "one-year"})

    def test_out_of_range_hsts_duration_fails_closed(self):
        with self.assertRaisesMessage(ImproperlyConfigured, "between 0 and 63072000"):
            load_security_settings({"DJANGO_SECURE_HSTS_SECONDS": "63072001"})

    def test_subdomain_hsts_requires_positive_duration(self):
        with self.assertRaisesMessage(
            ImproperlyConfigured, "HSTS subdomains require a positive HSTS duration"
        ):
            load_security_settings({"DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS": "true"})

    def test_unknown_environment_fails_closed(self):
        with self.assertRaisesMessage(
            ImproperlyConfigured, "DJANGO_ENVIRONMENT must be"
        ):
            load_security_settings({"DJANGO_ENVIRONMENT": "staging-ish"})

    def test_production_requires_explicit_hosts(self):
        with self.assertRaisesMessage(
            ImproperlyConfigured, "Production requires explicit DJANGO_ALLOWED_HOSTS"
        ):
            load_security_settings({"DJANGO_ENVIRONMENT": "production"})

    def test_production_requires_https_redirect(self):
        with self.assertRaisesMessage(
            ImproperlyConfigured, "Production requires DJANGO_SECURE_SSL_REDIRECT=true"
        ):
            load_security_settings(
                {
                    "DJANGO_ENVIRONMENT": "production",
                    "DJANGO_ALLOWED_HOSTS": "example.invalid",
                }
            )

    def test_production_requires_positive_hsts_duration(self):
        with self.assertRaisesMessage(
            ImproperlyConfigured,
            "Production requires a positive DJANGO_SECURE_HSTS_SECONDS",
        ):
            load_security_settings(
                {
                    "DJANGO_ENVIRONMENT": "production",
                    "DJANGO_ALLOWED_HOSTS": "example.invalid",
                    "DJANGO_SECURE_SSL_REDIRECT": "true",
                }
            )

    def test_valid_production_configuration_enables_secure_cookie_flags(self):
        config = load_security_settings(
            {
                "DJANGO_ENVIRONMENT": "production",
                "DJANGO_ALLOWED_HOSTS": "example.invalid",
                "DJANGO_SECURE_SSL_REDIRECT": "true",
                "DJANGO_SECURE_HSTS_SECONDS": "86400",
            }
        )

        self.assertTrue(config["ssl_redirect"])
        self.assertEqual(config["hsts_seconds"], 86400)
        self.assertTrue(config["session_cookie_secure"])
        self.assertTrue(config["csrf_cookie_secure"])
