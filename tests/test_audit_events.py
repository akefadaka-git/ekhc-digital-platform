"""Tests for privacy-minimized append-only audit event contracts."""

from dataclasses import FrozenInstanceError
from datetime import UTC, datetime
from uuid import uuid4

from django.test import SimpleTestCase

from audit.events import AuditEvent, AuditOutcome
from identity.references import AccountReference


class AuditEventTests(SimpleTestCase):
    def setUp(self):
        self.event = AuditEvent(
            action="document.read",
            resource_type="document",
            resource_reference="doc-ref-001",
            occurred_at=datetime(2026, 11, 12, 12, 0, tzinfo=UTC),
            correlation_id=uuid4(),
            outcome=AuditOutcome.SUCCEEDED,
            actor=AccountReference("account-ref-001"),
        )

    def test_event_has_generated_unique_id(self):
        other = AuditEvent(
            action="document.read",
            resource_type="document",
            resource_reference="doc-ref-001",
            occurred_at=datetime(2026, 11, 12, 12, 0, tzinfo=UTC),
            correlation_id=uuid4(),
            outcome=AuditOutcome.SUCCEEDED,
        )
        self.assertNotEqual(self.event.event_id, other.event_id)

    def test_event_is_immutable(self):
        with self.assertRaises(FrozenInstanceError):
            self.event.action = "document.write"

    def test_actor_is_optional_but_cannot_be_an_untyped_identity(self):
        self.assertIsNone(
            AuditEvent(
                action="system.health_check",
                resource_type="service",
                resource_reference="health",
                occurred_at=datetime(2026, 11, 12, 12, 0, tzinfo=UTC),
                correlation_id=uuid4(),
                outcome=AuditOutcome.SUCCEEDED,
            ).actor
        )
        with self.assertRaisesMessage(TypeError, "actor must be an AccountReference"):
            AuditEvent(
                action="system.health_check",
                resource_type="service",
                resource_reference="health",
                occurred_at=datetime(2026, 11, 12, 12, 0, tzinfo=UTC),
                correlation_id=uuid4(),
                outcome=AuditOutcome.SUCCEEDED,
                actor="someone",
            )

    def test_untrusted_action_text_is_rejected(self):
        with self.assertRaisesMessage(ValueError, "normalized event identifier"):
            AuditEvent(
                action="read document",
                resource_type="document",
                resource_reference="doc-ref-001",
                occurred_at=datetime(2026, 11, 12, 12, 0, tzinfo=UTC),
                correlation_id=uuid4(),
                outcome=AuditOutcome.SUCCEEDED,
            )

    def test_naive_event_timestamp_is_rejected(self):
        with self.assertRaisesMessage(ValueError, "timezone-aware"):
            AuditEvent(
                action="document.read",
                resource_type="document",
                resource_reference="doc-ref-001",
                occurred_at=datetime(2026, 11, 12, 12, 0),
                correlation_id=uuid4(),
                outcome=AuditOutcome.SUCCEEDED,
            )
