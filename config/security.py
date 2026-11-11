"""Validated, deployment-conscious security settings.

Proxy TLS termination is deliberately unsupported until the actual proxy chain,
header-stripping behavior, and network trust boundary are verified.
"""

_TRUE_VALUES = {"1", "true"}
_FALSE_VALUES = {"0", "false"}
_MAX_HSTS_SECONDS = 63_072_000


def _improperly_configured(message):
    from django.core.exceptions import ImproperlyConfigured

    return ImproperlyConfigured(message)


def _boolean(environ, name, default):
    raw_value = environ.get(name)
    if raw_value is None:
        return default

    normalized = raw_value.strip().lower()
    if normalized in _TRUE_VALUES:
        return True
    if normalized in _FALSE_VALUES:
        return False
    raise _improperly_configured(f"{name} must be exactly true/false or 1/0.")


def _hsts_seconds(environ):
    raw_value = environ.get("DJANGO_SECURE_HSTS_SECONDS", "0").strip()
    try:
        seconds = int(raw_value)
    except ValueError as exc:
        raise _improperly_configured(
            "DJANGO_SECURE_HSTS_SECONDS must be a whole number."
        ) from exc

    if not 0 <= seconds <= _MAX_HSTS_SECONDS:
        raise _improperly_configured(
            "DJANGO_SECURE_HSTS_SECONDS must be between 0 and 63072000."
        )
    return seconds


def load_security_settings(environ):
    """Return validated security settings without guessing deployment topology."""
    environment = environ.get("DJANGO_ENVIRONMENT", "development").strip().lower()
    if environment not in {"development", "test", "production"}:
        raise _improperly_configured(
            "DJANGO_ENVIRONMENT must be development, test, or production."
        )

    ssl_redirect = _boolean(environ, "DJANGO_SECURE_SSL_REDIRECT", False)
    hsts_seconds = _hsts_seconds(environ)
    hsts_include_subdomains = _boolean(
        environ, "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", False
    )

    if hsts_include_subdomains and hsts_seconds == 0:
        raise _improperly_configured(
            "HSTS subdomains require a positive HSTS duration."
        )

    if environment == "production":
        if not environ.get("DJANGO_ALLOWED_HOSTS", "").strip():
            raise _improperly_configured(
                "Production requires explicit DJANGO_ALLOWED_HOSTS."
            )
        if not ssl_redirect:
            raise _improperly_configured(
                "Production requires DJANGO_SECURE_SSL_REDIRECT=true."
            )
        if hsts_seconds == 0:
            raise _improperly_configured(
                "Production requires a positive DJANGO_SECURE_HSTS_SECONDS."
            )

    return {
        "environment": environment,
        "ssl_redirect": ssl_redirect,
        "hsts_seconds": hsts_seconds,
        "hsts_include_subdomains": hsts_include_subdomains,
        "session_cookie_secure": environment == "production",
        "csrf_cookie_secure": environment == "production",
    }
