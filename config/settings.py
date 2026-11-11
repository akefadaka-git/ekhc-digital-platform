"""Minimal, non-persistent settings for the EKHC OS foundation."""

import os

from config.runtime import load_runtime_settings
from config.security import load_security_settings

SECURITY = load_security_settings(os.environ)
DJANGO_ENVIRONMENT = SECURITY["environment"]
RUNTIME = load_runtime_settings(os.environ, DJANGO_ENVIRONMENT)
SECRET_KEY = RUNTIME["secret_key"]
ALLOWED_HOSTS = RUNTIME["allowed_hosts"]

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
