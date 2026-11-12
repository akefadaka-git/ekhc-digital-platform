"""Tests for metadata-only document version and access contracts."""

from datetime import UTC, datetime

from django.test import SimpleTestCase

from audit.records import (
    DenyAllDocumentAccess,
    DocumentAccessRequest,
    DocumentAction,
    DocumentMetadata,
    DocumentVersion,
)
from identity.references import AccountReference

NOW = datetime(2026, 11, 12, 12, 0, tzinfo=UTC)


class DocumentMetadataTests(SimpleTestCase):
    def test_valid_metadata_is_accepted(self):
        metadata = DocumentMetadata(
            document_reference="doc-ref-001",
            media_type="application/pdf",
            current_version=1,
            checksum_sha256="a" * 64,
            size_bytes=1024,
            created_at=NOW,
            updated_at=NOW,
        )
        self.assertEqual(metadata.current_version, 1)

    def test_invalid_media_type_is_rejected(self):
        with self.assertRaisesMessage(ValueError, "normalized MIME type"):
            DocumentMetadata(
                document_reference="doc-ref-001",
                media_type="PDF",
                current_version=1,
                checksum_sha256="a" * 64,
                size_bytes=1024,
                created_at=NOW,
                updated_at=NOW,
            )

    def test_updated_timestamp_cannot_precede_created(self):
        with self.assertRaisesMessage(ValueError, "must not precede"):
            DocumentMetadata(
                document_reference="doc-ref-001",
                media_type="application/pdf",
                current_version=1,
                checksum_sha256="a" * 64,
                size_bytes=1024,
                created_at=NOW,
                updated_at=datetime(2026, 11, 12, 11, 59, tzinfo=UTC),
            )

    def test_version_requires_positive_number_and_checksum(self):
        with self.assertRaisesMessage(ValueError, "version must be positive"):
            DocumentVersion(
                version=0,
                checksum_sha256="a" * 64,
                size_bytes=0,
                created_at=NOW,
            )
        with self.assertRaisesMessage(ValueError, "SHA-256 digest"):
            DocumentVersion(
                version=1,
                checksum_sha256="bad",
                size_bytes=0,
                created_at=NOW,
            )


class DocumentAccessBoundaryTests(SimpleTestCase):
    def test_access_is_denied_until_policy_is_configured(self):
        request = DocumentAccessRequest(
            actor=AccountReference("account-ref-001"),
            document_reference="doc-ref-001",
            action=DocumentAction.READ,
        )
        self.assertFalse(DenyAllDocumentAccess().allows(request))

    def test_untyped_actor_is_rejected(self):
        with self.assertRaisesMessage(TypeError, "actor must be an AccountReference"):
            DocumentAccessRequest(
                actor="account-ref-001",
                document_reference="doc-ref-001",
                action=DocumentAction.READ,
            )
