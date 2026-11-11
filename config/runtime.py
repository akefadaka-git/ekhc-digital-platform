"""Fail-closed validation for runtime secrets and host configuration."""

import ipaddress
import re

_HOST_LABEL = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$")
_WEAK_SECRET_MARKERS = (
    "change-me",
    "changeme",
    "placeholder",
    "not-for-production",
    "replace-me",
)


def _improperly_configured(message):
    from django.core.exceptions import ImproperlyConfigured

    return ImproperlyConfigured(message)


def _valid_host(host):
    candidate = host[1:] if host.startswith(".") else host
    if not candidate or len(candidate) > 253:
        return False

    try:
        ipaddress.ip_address(candidate)
        return True
    except ValueError:
        pass

    labels = candidate.split(".")
    return all(_HOST_LABEL.fullmatch(label) for label in labels)


def parse_allowed_hosts(raw_value):
    """Parse explicit DNS/IP hosts; reject wildcards, malformed and duplicate items."""
    if not isinstance(raw_value, str) or not raw_value.strip():
        raise _improperly_configured(
            "DJANGO_ALLOWED_HOSTS must contain explicit hostnames or IP addresses."
        )

    raw_hosts = raw_value.split(",")
    if any(not item.strip() for item in raw_hosts):
        raise _improperly_configured(
            "DJANGO_ALLOWED_HOSTS must not contain empty entries."
        )

    hosts = []
    seen = set()
    for item in raw_hosts:
        host = item.strip()
        normalized = host.lower()
        if "*" in host:
            raise _improperly_configured(
                "DJANGO_ALLOWED_HOSTS must contain explicit hostnames; "
                "wildcards are forbidden."
            )
        if any(character.isspace() for character in host) or not _valid_host(
            normalized
        ):
            raise _improperly_configured(
                "DJANGO_ALLOWED_HOSTS contains an invalid host entry."
            )
        if normalized in seen:
            raise _improperly_configured(
                "DJANGO_ALLOWED_HOSTS must not contain duplicate entries."
            )
        seen.add(normalized)
        hosts.append(host)

    return hosts


def load_runtime_settings(environ, environment):
    """Validate required runtime configuration without exposing secret values."""
    secret_key = environ.get("DJANGO_SECRET_KEY", "").strip()
    if not secret_key:
        raise _improperly_configured(
            "DJANGO_SECRET_KEY must be set; do not commit or log its value."
        )

    if environment == "production":
        normalized_secret = secret_key.lower()
        if (
            len(secret_key) < 50
            or any(character.isspace() for character in secret_key)
            or any(marker in normalized_secret for marker in _WEAK_SECRET_MARKERS)
        ):
            raise _improperly_configured(
                "Production DJANGO_SECRET_KEY must be a non-placeholder value "
                "of at least 50 non-whitespace characters."
            )

    default_hosts = "localhost,127.0.0.1,testserver"
    hosts = parse_allowed_hosts(environ.get("DJANGO_ALLOWED_HOSTS", default_hosts))
    return {"secret_key": secret_key, "allowed_hosts": hosts}
