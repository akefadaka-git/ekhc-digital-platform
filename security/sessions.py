"""Non-persistent authentication/session security contracts.

This module evaluates a supplied session observation. It does not authenticate
credentials, issue or rotate cookies, store sessions, or trust client timestamps.
A future provider must supply authenticated server-side observations and a
trusted clock before these contracts can govern real sessions.
"""

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Protocol

from identity.references import AccountReference


@dataclass(frozen=True, slots=True)
class SessionCookiePolicy:
    """Safe cookie requirements for a future browser-session adapter."""

    secure: bool = True
    http_only: bool = True
    same_site: str = "Lax"
    path: str = "/"
    domain: str | None = None

    def __post_init__(self) -> None:
        if not self.secure:
            raise ValueError("session cookies must require HTTPS.")
        if not self.http_only:
            raise ValueError("session cookies must be HttpOnly.")
        if self.same_site not in {"Strict", "Lax"}:
            raise ValueError("same_site must be Strict or Lax.")
        if self.path != "/":
            raise ValueError("session cookie path must be root-scoped.")
        if self.domain is not None:
            raise ValueError("session cookie domain must remain host-only.")


@dataclass(frozen=True, slots=True)
class SessionPolicy:
    idle_timeout: timedelta
    absolute_timeout: timedelta
    rotate_on_authentication: bool = True
    rotate_on_security_boundary_change: bool = True

    def __post_init__(self) -> None:
        if not isinstance(self.idle_timeout, timedelta) or not isinstance(
            self.absolute_timeout, timedelta
        ):
            raise TypeError("session timeouts must be timedeltas.")
        if self.idle_timeout <= timedelta(0):
            raise ValueError("idle_timeout must be positive.")
        if self.absolute_timeout <= timedelta(0):
            raise ValueError("absolute_timeout must be positive.")
        if self.idle_timeout > self.absolute_timeout:
            raise ValueError("idle_timeout must not exceed absolute_timeout.")
        if not self.rotate_on_authentication:
            raise ValueError("session rotation after authentication is mandatory.")
        if not self.rotate_on_security_boundary_change:
            raise ValueError(
                "session rotation after a security-boundary change is mandatory."
            )


@dataclass(frozen=True, slots=True)
class SessionObservation:
    """Trusted server-side facts; never construct from request-body timestamps."""

    account: AccountReference
    issued_at: datetime
    last_activity_at: datetime
    absolute_expires_at: datetime
    authenticated: bool
    revoked: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.account, AccountReference):
            raise TypeError("account must be an AccountReference.")
        for name in ("issued_at", "last_activity_at", "absolute_expires_at"):
            value = getattr(self, name)
            if not isinstance(value, datetime) or value.tzinfo is None:
                raise ValueError(f"{name} must be a timezone-aware datetime.")
        if self.last_activity_at < self.issued_at:
            raise ValueError("last_activity_at must not precede issued_at.")
        if self.absolute_expires_at <= self.issued_at:
            raise ValueError("absolute_expires_at must follow issued_at.")
        if not isinstance(self.authenticated, bool) or not isinstance(self.revoked, bool):
            raise TypeError("authenticated and revoked must be booleans.")


@dataclass(frozen=True, slots=True)
class SessionEvaluation:
    accepted: bool
    reason_code: str


class AuthenticationProvider(Protocol):
    """External verifier boundary; no password or token implementation is selected."""

    def authenticate(self, credential_exchange: bytes) -> AccountReference | None: ...


def evaluate_session(
    observation: SessionObservation,
    policy: SessionPolicy,
    *,
    now: datetime,
) -> SessionEvaluation:
    """Evaluate expiry/revocation against one injected trusted-time observation."""
    if not isinstance(observation, SessionObservation):
        raise TypeError("observation must be a SessionObservation.")
    if not isinstance(policy, SessionPolicy):
        raise TypeError("policy must be a SessionPolicy.")
    if not isinstance(now, datetime) or now.tzinfo is None:
        raise ValueError("now must be a timezone-aware trusted datetime.")
    if observation.revoked:
        reason = "SESSION_REVOKED"
    elif not observation.authenticated:
        reason = "SESSION_NOT_AUTHENTICATED"
    elif now < observation.issued_at or now < observation.last_activity_at:
        reason = "SESSION_TIME_OBSERVATION_INVALID"
    elif now >= observation.absolute_expires_at:
        reason = "SESSION_ABSOLUTE_TIMEOUT"
    elif now - observation.last_activity_at >= policy.idle_timeout:
        reason = "SESSION_IDLE_TIMEOUT"
    else:
        return SessionEvaluation(True, "SESSION_VALID")
    return SessionEvaluation(False, reason)


def utc_now() -> datetime:
    """Convenience clock for non-production callers; inject trusted time in tests."""
    return datetime.now(UTC)
