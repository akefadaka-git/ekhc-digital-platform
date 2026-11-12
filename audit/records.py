"""Document metadata, version, and access-policy interfaces without file storage."""

import re
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Protocol

from identity.references import AccountReference

_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_MEDIA_TYPE = re.compile(r"^[a-z0-9.+-]+/[a-z0-9.+-]+$")


class DocumentAction(StrEnum):
    READ = "read"
    WRITE = "write"
    DOWNLOAD = "download"
    DELETE = "delete"


@dataclass(frozen=True, slots=True)
class DocumentVersion:
    version: int
    checksum_sha256: str
    size_bytes: int
    created_at: datetime
    created_by: AccountReference | None = None

    def __post_init__(self) -> None:
        if isinstance(self.version, bool) or not isinstance(self.version, int):
            raise TypeError("version must be an integer.")
        if self.version < 1:
            raise ValueError("version must be positive.")
        if not isinstance(self.checksum_sha256, str) or not _SHA256.fullmatch(
            self.checksum_sha256
        ):
            raise ValueError("checksum_sha256 must be a lowercase SHA-256 digest.")
        if isinstance(self.size_bytes, bool) or not isinstance(self.size_bytes, int):
            raise TypeError("size_bytes must be an integer.")
        if self.size_bytes < 0:
            raise ValueError("size_bytes must not be negative.")
        if not isinstance(self.created_at, datetime) or self.created_at.tzinfo is None:
            raise ValueError("created_at must be timezone-aware.")
        if self.created_by is not None and not isinstance(
            self.created_by, AccountReference
        ):
            raise TypeError("created_by must be an AccountReference or None.")


@dataclass(frozen=True, slots=True)
class DocumentMetadata:
    document_reference: str
    media_type: str
    current_version: int
    checksum_sha256: str
    size_bytes: int
    created_at: datetime
    updated_at: datetime

    def __post_init__(self) -> None:
        if (
            not isinstance(self.document_reference, str)
            or not self.document_reference
            or self.document_reference != self.document_reference.strip()
        ):
            raise ValueError("document_reference must be non-empty and normalized.")
        if not isinstance(self.media_type, str) or not _MEDIA_TYPE.fullmatch(
            self.media_type
        ):
            raise ValueError("media_type must be a normalized MIME type.")
        if (
            isinstance(self.current_version, bool)
            or not isinstance(self.current_version, int)
            or self.current_version < 1
        ):
            raise ValueError("current_version must be a positive integer.")
        if not isinstance(self.checksum_sha256, str) or not _SHA256.fullmatch(
            self.checksum_sha256
        ):
            raise ValueError("checksum_sha256 must be a lowercase SHA-256 digest.")
        if isinstance(self.size_bytes, bool) or not isinstance(self.size_bytes, int):
            raise TypeError("size_bytes must be an integer.")
        if self.size_bytes < 0:
            raise ValueError("size_bytes must not be negative.")
        if (
            not isinstance(self.created_at, datetime)
            or self.created_at.tzinfo is None
            or not isinstance(self.updated_at, datetime)
            or self.updated_at.tzinfo is None
        ):
            raise ValueError("document timestamps must be timezone-aware.")
        if self.updated_at < self.created_at:
            raise ValueError("updated_at must not precede created_at.")


@dataclass(frozen=True, slots=True)
class DocumentAccessRequest:
    actor: AccountReference
    document_reference: str
    action: DocumentAction

    def __post_init__(self) -> None:
        if not isinstance(self.actor, AccountReference):
            raise TypeError("actor must be an AccountReference.")
        if (
            not isinstance(self.document_reference, str)
            or not self.document_reference
            or self.document_reference != self.document_reference.strip()
        ):
            raise ValueError("document_reference must be non-empty and normalized.")
        if not isinstance(self.action, DocumentAction):
            raise TypeError("action must be a DocumentAction.")


class DocumentAccessPolicy(Protocol):
    """Provider-neutral access boundary; no role or office mapping is defined."""

    def allows(self, request: DocumentAccessRequest) -> bool: ...


class DocumentMetadataStore(Protocol):
    """Metadata-only store contract; file bytes and retention are out of scope."""

    def get(self, document_reference: str) -> DocumentMetadata | None: ...

    def append_version(self, document_reference: str, version: DocumentVersion) -> None: ...


class DenyAllDocumentAccess:
    """Safe default until an independently approved access policy is supplied."""

    def allows(self, request: DocumentAccessRequest) -> bool:
        if not isinstance(request, DocumentAccessRequest):
            raise TypeError("request must be a DocumentAccessRequest.")
        return False
