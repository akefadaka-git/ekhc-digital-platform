"""Request-scoped Amharic-first platform language negotiation."""

from django.conf import settings
from django.utils.cache import patch_vary_headers


def resolve_platform_language(accept_language):
    """Choose a supported platform language from an Accept-Language header."""
    supported = set(settings.PLATFORM_SUPPORTED_LANGUAGES)
    default = settings.PLATFORM_DEFAULT_LANGUAGE
    candidates = []

    for position, item in enumerate(accept_language.split(",")):
        parts = [part.strip() for part in item.split(";")]
        language = parts[0].lower().replace("_", "-")
        if not language or language == "*":
            continue

        quality = 1.0
        for parameter in parts[1:]:
            key, separator, value = parameter.partition("=")
            if separator and key.strip().lower() == "q":
                try:
                    quality = float(value.strip())
                except ValueError:
                    quality = 0.0
                break

        if not 0.0 < quality <= 1.0:
            continue

        primary_language = language.split("-", maxsplit=1)[0]
        if primary_language in supported:
            candidates.append((-quality, position, primary_language))

    if candidates:
        return min(candidates)[2]
    return default


class PlatformLanguageMiddleware:
    """Attach the negotiated platform language to each request and response."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        language = resolve_platform_language(request.headers.get("Accept-Language", ""))
        request.LANGUAGE_CODE = language
        response = self.get_response(request)
        response.headers["Content-Language"] = language
        patch_vary_headers(response, ("Accept-Language",))
        return response
