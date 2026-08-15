"""Canonical, connector-neutral models used by the reference runtime."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from hashlib import sha256
import json
from typing import Any


class EventKind(StrEnum):
    """The minimum cross-connector vocabulary for observed changes."""

    CREATED = "created"
    UPDATED = "updated"
    DELETED = "deleted"
    LINKED = "linked"
    UNLINKED = "unlinked"


class ActionStatus(StrEnum):
    """Lifecycle state of a proposed connector action."""

    PLANNED = "planned"
    AWAITING_APPROVAL = "awaiting_approval"
    EXECUTED = "executed"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class ResourceRef:
    """Stable reference to one resource in an external system."""

    connector: str
    resource_type: str
    external_id: str
    url: str | None = None

    def __post_init__(self) -> None:
        for name in ("connector", "resource_type", "external_id"):
            value = getattr(self, name)
            if not value or not value.strip():
                raise ValueError(f"{name} must be a non-empty string")

    @property
    def key(self) -> str:
        """Return a connector-neutral identity key."""

        return f"{self.connector}:{self.resource_type}:{self.external_id}"


@dataclass(frozen=True, slots=True)
class GrimoireEvent:
    """Normalized statement that something happened to an external resource."""

    source: ResourceRef
    kind: EventKind
    occurred_at: datetime
    payload: Mapping[str, Any] = field(default_factory=dict)
    provenance: Mapping[str, Any] = field(default_factory=dict)
    schema_version: str = "0.1.0"
    event_id: str | None = None

    def __post_init__(self) -> None:
        occurred_at = self.occurred_at
        if occurred_at.tzinfo is None:
            occurred_at = occurred_at.replace(tzinfo=UTC)
            object.__setattr__(self, "occurred_at", occurred_at)

        if self.event_id is None:
            digest = sha256(self._canonical_bytes()).hexdigest()[:24]
            object.__setattr__(self, "event_id", f"evt_{digest}")

    def _canonical_bytes(self) -> bytes:
        body = {
            "schema_version": self.schema_version,
            "source": asdict(self.source),
            "kind": self.kind.value,
            "occurred_at": self.occurred_at.astimezone(UTC).isoformat(),
            "payload": self.payload,
            "provenance": self.provenance,
        }
        return json.dumps(body, sort_keys=True, separators=(",", ":"), default=str).encode()

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation."""

        return {
            "schema_version": self.schema_version,
            "event_id": self.event_id,
            "source": asdict(self.source),
            "kind": self.kind.value,
            "occurred_at": self.occurred_at.astimezone(UTC).isoformat(),
            "payload": dict(self.payload),
            "provenance": dict(self.provenance),
        }


@dataclass(frozen=True, slots=True)
class ProposedAction:
    """A connector write that can be inspected before it is executed."""

    target: ResourceRef
    action: str
    changes: Mapping[str, Any]
    reason: str
    requires_approval: bool = True
    action_id: str | None = None

    def __post_init__(self) -> None:
        if not self.action.strip():
            raise ValueError("action must be a non-empty string")
        if not self.reason.strip():
            raise ValueError("reason must explain why the action was proposed")

        if self.action_id is None:
            body = {
                "target": asdict(self.target),
                "action": self.action,
                "changes": self.changes,
                "reason": self.reason,
                "requires_approval": self.requires_approval,
            }
            digest = sha256(
                json.dumps(body, sort_keys=True, separators=(",", ":"), default=str).encode()
            ).hexdigest()[:24]
            object.__setattr__(self, "action_id", f"act_{digest}")


@dataclass(frozen=True, slots=True)
class ActionRecord:
    """Append-only ledger record for one planned or executed action."""

    event_id: str
    action_id: str
    target: ResourceRef
    status: ActionStatus
    recorded_at: datetime
    detail: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "action_id": self.action_id,
            "target": asdict(self.target),
            "status": self.status.value,
            "recorded_at": self.recorded_at.astimezone(UTC).isoformat(),
            "detail": dict(self.detail),
        }
