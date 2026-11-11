"""Minimal, non-persistent settings for the first EKHC OS increment."""

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

# No product apps, middleware, database, ORM persistence, or migrations are enabled.
INSTALLED_APPS = []
MIDDLEWARE = []
TEMPLATES = []

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
