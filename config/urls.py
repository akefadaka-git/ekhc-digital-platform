"""The only route in the first increment is a non-sensitive health check."""

from django.urls import path

from health.views import health

urlpatterns = [path("health/", health, name="health")]
