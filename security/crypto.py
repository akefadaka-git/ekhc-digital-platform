"""Provider-neutral envelope-encryption and key-management contracts.

No cryptographic primitive or key provider is implemented here. Production adapters
must pass independent AES-256-GCM and KMS/HSM conformance tests before activation.
"""

import hashlib
import re
import secrets
from dataclasses import dataclass, field
from typing import Protocol

AES_256_GCM_SUITE = "AES-256-GCM"
AES_GCM_NONCE_BYTES = 12
AES_GCM_TAG_BYTES = 16
AES_256_KEY_BYTES = 32


@dataclass(frozen=True, slots=True)
class GeneratedDataKey:
    plaintext_key: bytearray = field(repr=False, compare=False)
    wrapped_key: bytes
    key_reference: str
    key_version: str

    def __post_init__(self) -> None:
        if (
            not isinstance(self.plaintext_key, bytearray)
            or len(self.plaintext_key) != AES_256_KEY_BYTES
        ):
            raise ValueError("plaintext data key must be a 32-byte mutable buffer.")
        if not isinstance(self.wrapped_key, bytes) or not self.wrapped_key:
            raise ValueError("wrapped data key must be non-empty bytes.")
        for name in ("key_reference", "key_version"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value or value != value.strip():
                raise ValueError(f"{name} must be a non-empty normalized string.")


@dataclass(frozen=True, slots=True)
class EncryptionEnvelope:
    ciphertext: bytes
    nonce: bytes
    wrapped_key: bytes
    key_reference: str
    key_version: str
    algorithm_suite: str
    aad_sha256: str

    def __post_init__(self) -> None:
        if (
            not isinstance(self.ciphertext, bytes)
            or len(self.ciphertext) < AES_GCM_TAG_BYTES
        ):
            raise ValueError("ciphertext must include an authentication tag.")
        if not isinstance(self.nonce, bytes) or len(self.nonce) != AES_GCM_NONCE_BYTES:
            raise ValueError("AES-GCM nonce must contain 12 bytes.")
        if not isinstance(self.wrapped_key, bytes) or not self.wrapped_key:
            raise ValueError("wrapped_key must be non-empty bytes.")
        if not isinstance(self.key_reference, str) or not self.key_reference:
            raise ValueError("key_reference must be non-empty.")
        if not isinstance(self.key_version, str) or not self.key_version:
            raise ValueError("key_version must be non-empty.")
        if self.algorithm_suite != AES_256_GCM_SUITE:
            raise ValueError("unsupported algorithm suite.")
        if not isinstance(self.aad_sha256, str) or not re.fullmatch(
            r"[0-9a-f]{64}", self.aad_sha256
        ):
            raise ValueError("aad_sha256 must be a lowercase SHA-256 digest.")


class KeyEncryptionProvider(Protocol):
    """KMS/HSM boundary. KEK material never enters this application interface."""

    def generate_data_key(self, key_reference: str) -> GeneratedDataKey: ...

    def unwrap_data_key(self, wrapped_key: bytes, key_reference: str) -> bytearray: ...

    def rewrap_data_key(
        self, wrapped_key: bytes, old_key_reference: str, new_key_reference: str
    ) -> tuple[bytes, str]: ...


class PayloadCipher(Protocol):
    """Authenticated encryption primitive; implementation must be AES-256-GCM."""

    def encrypt(
        self, plaintext: bytes, key: bytes, nonce: bytes, associated_data: bytes
    ) -> bytes: ...

    def decrypt(
        self, ciphertext: bytes, key: bytes, nonce: bytes, associated_data: bytes
    ) -> bytes: ...


class EncryptedObjectStore(Protocol):
    """Private object-store adapter accepts ciphertext only."""

    def put_staged(self, object_reference: str, ciphertext: bytes) -> str: ...

    def verify(
        self, staged_reference: str, expected_sha256: str, expected_size: int
    ) -> bool: ...

    def promote(
        self, staged_reference: str, immutable_object_reference: str
    ) -> None: ...

    def get(self, immutable_object_reference: str) -> bytes: ...


def _zeroize(value: bytearray) -> None:
    for index in range(len(value)):
        value[index] = 0


def encrypt_payload(
    plaintext: bytes,
    key_provider: KeyEncryptionProvider,
    cipher: PayloadCipher,
    *,
    key_reference: str,
    associated_data: bytes,
) -> EncryptionEnvelope:
    """Create a fresh per-payload DEK and AES-GCM envelope via injected adapters."""
    if not isinstance(plaintext, bytes):
        raise TypeError("plaintext must be bytes.")
    if not isinstance(associated_data, bytes) or not associated_data:
        raise ValueError("associated_data must be non-empty bytes.")
    generated = key_provider.generate_data_key(key_reference)
    try:
        nonce = secrets.token_bytes(AES_GCM_NONCE_BYTES)
        ciphertext = cipher.encrypt(
            plaintext, bytes(generated.plaintext_key), nonce, associated_data
        )
        return EncryptionEnvelope(
            ciphertext=ciphertext,
            nonce=nonce,
            wrapped_key=generated.wrapped_key,
            key_reference=generated.key_reference,
            key_version=generated.key_version,
            algorithm_suite=AES_256_GCM_SUITE,
            aad_sha256=hashlib.sha256(associated_data).hexdigest(),
        )
    finally:
        _zeroize(generated.plaintext_key)


def decrypt_payload(
    envelope: EncryptionEnvelope,
    key_provider: KeyEncryptionProvider,
    cipher: PayloadCipher,
    *,
    associated_data: bytes,
) -> bytes:
    """Decrypt only when the caller supplies the exact authenticated AAD."""
    if not isinstance(envelope, EncryptionEnvelope):
        raise TypeError("envelope must be an EncryptionEnvelope.")
    if not isinstance(associated_data, bytes) or not associated_data:
        raise ValueError("associated_data must be non-empty bytes.")
    if hashlib.sha256(associated_data).hexdigest() != envelope.aad_sha256:
        raise ValueError("associated_data does not match the encryption envelope.")
    plaintext_key = key_provider.unwrap_data_key(
        envelope.wrapped_key, envelope.key_reference
    )
    if (
        not isinstance(plaintext_key, bytearray)
        or len(plaintext_key) != AES_256_KEY_BYTES
    ):
        raise ValueError("KMS provider returned an invalid data key.")
    try:
        return cipher.decrypt(
            envelope.ciphertext,
            bytes(plaintext_key),
            envelope.nonce,
            associated_data,
        )
    finally:
        _zeroize(plaintext_key)
