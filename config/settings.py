"""Minimal, non-persistent settings for the EKHC OS foundation."""

import os

from django.core.exceptions import ImproperlyConfigured

from config.security import load_security_settings

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "").strip()
if not SECRET_KEY:
    raise ImproperlyConfigured(
        "DJANGO_SECRET_KEY must be set; do not commit or log its value."
    )

_raw_allowed_hosts = os.environ.get(
    "DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1,testserver"
)
ALLOWED_HOSTS = [host.strip() for host in _raw_allowed_hosts.split(",") if host.strip()]
if not ALLOWED_HOSTS or "*" in ALLOWED_HOSTS:
    raise ImproperlyConfigured(
        "DJANGO_ALLOWED_HOSTS must contain explicit hostnames; wildcards are forbidden."
    )

SECURITY = load_security_settings(os.environ)
DJANGO_ENVIRONMENT = SECURITY["environment"]

DEBUG = False
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# No product apps, database, ORM persistence, or migrations are enabled.
INSTALLED_APPS = []
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "config.observability.RequestCorrelationLoggingMiddleware",
    "config.localization.PlatformLanguageMiddleware",
]
TEMPLATES = []

# Django's internal translation fallback remains English because Django
# doesn't ship an Amharic catalogue. Platform language negotiation is handled
# separately and defaults to Amharic without claiming translated UI content.
LANGUAGE_CODE = "en"
PLATFORM_DEFAULT_LANGUAGE = "am"
PLATFORM_SUPPORTED_LANGUAGES = ("am", "en")
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Response hardening is safe without assuming a deployment hostname or proxy.
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
SECURE_REFERRER_POLICY = "same-origin"
SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin"

# HTTPS/HSTS are explicit deployment settings. Production startup validation
# requires both; development/test do not redirect or emit HSTS.
SECURE_SSL_REDIRECT = SECURITY["ssl_redirect"]
SECURE_HSTS_SECONDS = SECURITY["hsts_seconds"]
SECURE_HSTS_INCLUDE_SUBDOMAINS = SECURITY["hsts_include_subdomains"]
SECURE_HSTS_PRELOAD = False
SESSION_COOKIE_SECURE = SECURITY["session_cookie_secure"]
CSRF_COOKIE_SECURE = SECURITY["csrf_cookie_secure"]

# Do not trust X-Forwarded-* headers until the real proxy chain and its
# header-sanitization behavior have been independently verified.
SECURE_PROXY_SSL_HEADER = None
USE_X_FORWARDED_HOST = False

# Operational logs are structured and deliberately exclude paths, query strings,
# headers, bodies, user identifiers, and arbitrary log messages/extra fields.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "request_context": {
            "()": "config.observability.RequestContextFilter",
        },
    },
    "formatters": {
        "safe_json": {
            "()": "config.observability.SafeJsonFormatter",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "filters": ["request_context"],
            "formatter": "safe_json",
        },
    },
    "loggers": {
        "ekhc.request": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
