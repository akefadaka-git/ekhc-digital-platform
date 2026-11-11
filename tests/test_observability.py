"""Tests for request correlation and sensitive-data-safe structured logs."""

import json
import logging
from uuid import UUID

from django.test import SimpleTestCase

from config.observability import RequestContextFilter, SafeJsonFormatter, _request_id


class RequestCorrelationTests(SimpleTestCase):
    def test_response_contains_server_generated_request_id(self):
        response = self.client.get("/health/")
        request_id = response["X-Request-ID"]

        self.assertEqual(str(UUID(request_id)), request_id)
        self.assertEqual(response["Content-Language"], "am")

    def test_untrusted_incoming_request_id_is_not_reflected(self):
        response = self.client.get(
            "/health/",
            HTTP_X_REQUEST_ID="attacker-controlled-value",
        )

        self.assertNotEqual(response["X-Request-ID"], "attacker-controlled-value")
        self.assertEqual(str(UUID(response["X-Request-ID"])), response["X-Request-ID"])


class StructuredLogPrivacyTests(SimpleTestCase):
    def test_formatter_emits_only_allowlisted_operational_fields(self):
        record = logging.makeLogRecord(
            {
                "name": "ekhc.request",
                "levelno": logging.INFO,
                "levelname": "INFO",
                "msg": "password=hunter2 bearer=top-secret",
                "args": (),
                "request_id": "a5df7f5c-cc83-46c8-8c98-5cb4d85a7d8f",
                "method": "GET",
                "status_code": 200,
                "duration_ms": 1.25,
                "password": "hunter2",
                "authorization": "Bearer top-secret",
                "query_string": "email=person@example.invalid",
                "body": "private payload",
            }
        )
        context_token = _request_id.set("a5df7f5c-cc83-46c8-8c98-5cb4d85a7d8f")
        try:
            RequestContextFilter().filter(record)
            rendered = SafeJsonFormatter().format(record)
        finally:
            _request_id.reset(context_token)
        payload = json.loads(rendered)

        self.assertEqual(payload["event"], "http_request_completed")
        self.assertEqual(payload["method"], "GET")
        self.assertEqual(payload["status_code"], 200)
        self.assertEqual(payload["request_id"], "a5df7f5c-cc83-46c8-8c98-5cb4d85a7d8f")
        for sensitive_value in (
            "hunter2",
            "top-secret",
            "person@example.invalid",
            "private payload",
            "password",
            "authorization",
            "query_string",
        ):
            self.assertNotIn(sensitive_value, rendered)

    def test_formatter_rejects_untrusted_method_text(self):
        record = logging.makeLogRecord(
            {
                "name": "ekhc.request",
                "levelno": logging.INFO,
                "levelname": "INFO",
                "msg": "ignored",
                "method": "GET\\npassword=secret",
                "status_code": 200,
                "duration_ms": 2,
            }
        )

        payload = json.loads(SafeJsonFormatter().format(record))
        self.assertEqual(payload["method"], "OTHER")
