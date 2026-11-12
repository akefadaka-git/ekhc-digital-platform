"""Opaque, non-persistent references separating people from accounts.

These types do not authenticate a person, establish membership, or grant authority.
They deliberately carry no organizational semantics and are not Django models.
"""

from dataclasses import dataclass

_MAX_REFERENCE_LENGTH = 128


def _validate_reference(value: str, field_name: str) -> None:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string.")
    if not value or value != value.strip():
        raise ValueError(f"{field_name} must be non-empty and have no outer whitespace.")
    if len(value) > _MAX_REFERENCE_LENGTH:
        raise ValueError(f"{field_name} must not exceed {_MAX_REFERENCE_LENGTH} characters.")
    if any(character.isspace() for character in value):
        raise ValueError(f"{field_name} must not contain whitespace.")


@dataclass(frozen=True, slots=True)
class PersonReference:
    """Opaque reference to a person record; not proof of membership or identity."""

    value: str

    def __post_init__(self) -> None:
        _validate_reference(self.value, "Person reference")


@dataclass(frozen=True, slots=True)
class AccountReference:
    """Opaque reference to an application account; not an authenticated session."""

    value: str

    def __post_init__(self) -> None:
        _validate_reference(self.value, "Account reference")


@dataclass(frozen=True, slots=True)
class IdentityLink:
    """Explicit typed link between a person reference and an account reference.

    Persistence, verification, lifecycle, and approval are intentionally outside
    this value object. A link must never be inferred from matching string values.
    """

    person: PersonReference
    account: AccountReference

    def __post_init__(self) -> None:
        if not isinstance(self.person, PersonReference):
            raise TypeError("person must be a PersonReference.")
        if not isinstance(self.account, AccountReference):
            raise TypeError("account must be an AccountReference.")
