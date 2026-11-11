"""Non-sensitive health endpoint; it does not inspect external dependencies."""

from django.http import JsonResponse
from django.views.decorators.http import require_GET


@require_GET
def health(_request):
    """Report that the Django process can serve requests, without data disclosure."""
    response = JsonResponse({"status": "ok"})
    response["Cache-Control"] = "no-store"
    response["X-Content-Type-Options"] = "nosniff"
    return response
