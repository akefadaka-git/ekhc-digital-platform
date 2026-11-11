"""Regression guards for the intentionally absent auth and data-access surface."""

from django.conf import settings
from django.test import SimpleTestCase
from django.urls import get_resolver


class NoAuthenticationOrProtectedDataSurfaceTests(SimpleTestCase):
    """Keep the current foundation non-authenticated and non-persistent."""

    def test_no_product_or_authentication_apps_are_installed(self):
        self.assertEqual(settings.INSTALLED_APPS, [])

    def test_no_usable_database_is_configured(self):
        database = settings.DATABASES["default"]
        self.assertEqual(database["ENGINE"], "django.db.backends.dummy")
        self.assertEqual(database["NAME"], "")

    def test_health_is_the_only_registered_route(self):
        patterns = get_resolver().url_patterns

        self.assertEqual(len(patterns), 1)
        health_pattern = patterns[0]
        self.assertEqual(str(health_pattern.pattern), "health/")
        self.assertEqual(health_pattern.name, "health")
        self.assertEqual(health_pattern.callback.__module__, "health.views")

    def test_common_auth_and_data_routes_are_not_resolvable(self):
        from django.urls import Resolver404, resolve

        forbidden_paths = (
            "/login/",
            "/logout/",
            "/token/",
            "/accounts/",
            "/members/",
            "/organizations/",
            "/api/",
        )

        for path in forbidden_paths:
            with self.subTest(path=path):
                with self.assertRaises(Resolver404):
                    resolve(path)
