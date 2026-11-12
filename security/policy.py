"""Authorization request and fail-closed decision boundary.

No institutional roles, hierarchy, office mandates, or permission grants are
configured here. Until authoritative policy is approved and implemented, every
request is denied.
"""

from dataclasses import dataclass
from enum import StrEnum

from identity.references import AccountReference


class Decision(StrEnum):
    ALLOW = "allow"
    DENY = "deny"


@dataclass(frozen=True, slots=True)
class AuthorizationRequest:
    """A request envelope with opaque resource/scope references only."""

    actor: AccountReference
    action: str
    resource_type: str
    resource_reference: str
    scope_reference: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.actor, AccountReference):
            raise TypeError("actor must be an AccountReference.")
        for name in ("action", "resource_type", "resource_reference"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value or value != value.strip():
                raise ValueError(
                    f"{name} must be a non-empty string without outer whitespace."
                )
        if self.scope_reference is not None and (
            not isinstance(self.scope_reference, str)
            or not self.scope_reference
            or self.scope_reference != self.scope_reference.strip()
        ):
            raise ValueError("scope_reference must be absent or a non-empty string.")


@dataclass(frozen=True, slots=True)
class AuthorizationResult:
    decision: Decision
    reason_code: str


def evaluate_authorization(request: AuthorizationRequest) -> AuthorizationResult:
    """Deny until an independently approved policy evaluator is configured."""
    if not isinstance(request, AuthorizationRequest):
        raise TypeError("request must be an AuthorizationRequest.")
    return AuthorizationResult(
        decision=Decision.DENY,
        reason_code="AUTHORIZATION_POLICY_NOT_CONFIGURED",
    )
