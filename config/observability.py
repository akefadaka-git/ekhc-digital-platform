"""Request correlation and privacy-minimizing structured request logs."""

from __future__ import annotations

import json
import logging
import re
import time
from contextvars import ContextVar
from datetime import UTC, datetime
from uuid import uuid4

_request_id: ContextVar[str] = ContextVar("ekhc_request_id", default="-")
_METHOD_PATTERN = re.compile(r"^[A-Z]{1,16}$")


class RequestContextFilter(logging.Filter):
    """Attach the active server-generated request ID to log records."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = _request_id.get()
        return True


class SafeJsonFormatter(logging.Formatter):
    """Serialize an allowlist of operational fields; never serialize raw messages."""

    def format(self, record: logging.LogRecord) -> str:
        method = getattr(record, "method", "")
        method = (
            method
            if isinstance(method, str) and _METHOD_PATTERN.fullmatch(method)
            else "OTHER"
        )
        status_code = getattr(record, "status_code", None)
        if not isinstance(status_code, int) or isinstance(status_code, bool):
            status_code = None
        duration_ms = getattr(record, "duration_ms", None)
        if not isinstance(duration_ms, (int, float)) or isinstance(duration_ms, bool):
            duration_ms = None

        payload = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "event": "http_request_completed",
            "request_id": getattr(record, "request_id", "-"),
            "method": method,
            "status_code": status_code,
            "duration_ms": round(duration_ms, 3) if duration_ms is not None else None,
            "exception_type": getattr(record, "exception_type", None),
        }
        return json.dumps(payload, separators=(",", ":"), ensure_ascii=True)


class RequestCorrelationLoggingMiddleware:
    """Generate a fresh correlation ID and emit a data-minimized completion event."""

    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger("ekhc.request")

    def __call__(self, request):
        request_id = str(uuid4())
        request.request_id = request_id
        context_token = _request_id.set(request_id)
        started = time.perf_counter()
        response = None
        exception_type = None

        try:
            response = self.get_response(request)
            response.headers["X-Request-ID"] = request_id
            return response
        except Exception as exc:
            exception_type = type(exc).__name__
            raise
        finally:
            duration_ms = (time.perf_counter() - started) * 1000
            self.logger.info(
                "http_request_completed",
                extra={
                    "method": request.method.upper()[:16],
                    "status_code": (
                        response.status_code if response is not None else None
                    ),
                    "duration_ms": duration_ms,
                    "exception_type": exception_type,
                },
            )
            _request_id.reset(context_token)
