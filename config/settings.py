"""Minimal, non-persistent settings for the EKHC OS foundation."""

import os

from django.core.exceptions import ImproperlyConfigured

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

DEBUG = False
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# No product apps, database, ORM persistence, or migrations are enabled.
INSTALLED_APPS = []
MIDDLEWARE = [
    "django.middleware.locale.LocaleMiddleware",
]
TEMPLATES = []

# Request-scoped language negotiation: Amharic is the default; English is
# available as a supported preference. No user preference is persisted.
LANGUAGE_CODE = "am"
LANGUAGES = [
    ("am", "አማርኛ"),
    ("en", "English"),
]
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
