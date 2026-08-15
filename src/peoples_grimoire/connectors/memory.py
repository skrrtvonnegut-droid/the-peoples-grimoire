"""In-memory connector used by examples and conformance tests."""

from __future__ import annotations

from dataclasses import dataclass, field

from peoples_grimoire.models import ProposedAction

from .base import ExecutionResult
from .capabilities import (
    ConnectorCapability,
    ConnectorManifest,
    ConnectorOperation,
    RedactionMode,
    RetryPolicy,
)


def _default_manifest(name: str) -> ConnectorManifest:
    return ConnectorManifest(
        name=name,
        version="0.0.0",
        protocol_versions=frozenset({"0.1"}),
        resource_types=frozenset({"page", "record"}),
        capabilities=(
            ConnectorCapability(
                action="update_properties",
                operation=ConnectorOperation.UPDATE,
                resource_types=frozenset({"page"}),
                idempotent=True,
                conditional_updates=True,
                requires_approval=True,
            ),
            ConnectorCapability(
                action="record",
                operation=ConnectorOperation.UPDATE,
                resource_types=frozenset({"record"}),
                idempotent=True,
                requires_approval=False,
            ),
        ),
        authentication_methods=frozenset({"none"}),
        minimum_permissions=frozenset(),
        supports_polling=False,
        supports_webhooks=False,
        rate_limit_strategy="none",
        retry_policy=RetryPolicy(strategy="none", max_attempts=1),
        sensitive_fields=frozenset({"title", "body", "content", "url"}),
        data_classes=frozenset({"synthetic"}),
        default_redaction=RedactionMode.FINGERPRINT,
        deletion_behavior="none",
        recovery_supported=True,
        fixtures=frozenset({"synthetic/recording"}),
        conformance_tests=frozenset({"manifest", "dry_run", "approval", "execute"}),
    )


@dataclass(slots=True)
class RecordingConnector:
    """Record explicitly declared actions without touching an external SaaS API."""

    name: str
    manifest: ConnectorManifest | None = None
    granted_permissions: frozenset[str] = field(default_factory=frozenset)
    actions: list[ProposedAction] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.manifest is None:
            self.manifest = _default_manifest(self.name)
        if self.manifest.name != self.name:
            raise ValueError("connector name must match manifest name")
        self.granted_permissions = frozenset(self.granted_permissions)

    def execute(self, action: ProposedAction) -> ExecutionResult:
        self.actions.append(action)
        return ExecutionResult(
            external_id=action.target.external_id,
            url=action.target.url,
            detail={"recorded": True, "connector": self.name},
            safe_detail_fields=frozenset({"recorded", "connector"}),
        )
