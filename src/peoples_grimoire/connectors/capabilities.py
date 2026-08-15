"""Machine-readable connector capabilities and recipe permission checks."""

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from peoples_grimoire.models import ProposedAction

PROTOCOL_VERSION = "0.1"
MANIFEST_SCHEMA_VERSION = "0.1.0"

_NAME_PATTERN = re.compile(r"^[a-z][a-z0-9_-]*$")
_VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+(?:[-+][A-Za-z0-9.-]+)?$")


class CapabilityContractError(ValueError):
    """Raised when a connector manifest violates the protocol contract."""


class ConnectorOperation(StrEnum):
    """Operations a connector may explicitly declare."""

    READ = "read"
    OBSERVE = "observe"
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"

    @property
    def is_write(self) -> bool:
        return self in {
            ConnectorOperation.CREATE,
            ConnectorOperation.UPDATE,
            ConnectorOperation.DELETE,
        }


class RedactionMode(StrEnum):
    """Default handling for private connector fields."""

    OMIT = "omit"
    FINGERPRINT = "fingerprint"


@dataclass(frozen=True, slots=True)
class RetryPolicy:
    """Connector-neutral retry behavior."""

    strategy: str = "exponential"
    max_attempts: int = 5
    honors_retry_after: bool = True

    def __post_init__(self) -> None:
        if self.strategy not in {"none", "fixed", "exponential"}:
            raise CapabilityContractError(f"unsupported retry strategy: {self.strategy!r}")
        if self.max_attempts < 1:
            raise CapabilityContractError("max_attempts must be at least 1")


@dataclass(frozen=True, slots=True)
class ConnectorCapability:
    """One exact connector action and the authority it requires."""

    action: str
    operation: ConnectorOperation
    resource_types: frozenset[str]
    required_permissions: frozenset[str] = field(default_factory=frozenset)
    idempotent: bool = False
    conditional_updates: bool = False
    irreversible: bool = False
    requires_approval: bool = True

    def __post_init__(self) -> None:
        action = self.action.strip()
        resource_types = frozenset(value.strip() for value in self.resource_types if value.strip())
        permissions = frozenset(
            value.strip() for value in self.required_permissions if value.strip()
        )
        object.__setattr__(self, "action", action)
        object.__setattr__(self, "resource_types", resource_types)
        object.__setattr__(self, "required_permissions", permissions)

        if not action:
            raise CapabilityContractError("capability action must be non-empty")
        if not resource_types:
            raise CapabilityContractError(f"{action!r} must declare at least one resource type")
        if not self.operation.is_write and self.irreversible:
            raise CapabilityContractError("read and observe capabilities cannot be irreversible")
        if self.conditional_updates and self.operation is not ConnectorOperation.UPDATE:
            raise CapabilityContractError(
                "conditional_updates is valid only for update capabilities"
            )

    def supports(self, *, action: str, resource_type: str) -> bool:
        return self.action == action and resource_type in self.resource_types

    def to_dict(self) -> dict[str, Any]:
        return {
            "action": self.action,
            "operation": self.operation.value,
            "resource_types": sorted(self.resource_types),
            "required_permissions": sorted(self.required_permissions),
            "idempotent": self.idempotent,
            "conditional_updates": self.conditional_updates,
            "irreversible": self.irreversible,
            "requires_approval": self.requires_approval,
        }


@dataclass(frozen=True, slots=True)
class CapabilityRequirement:
    """Authority requested by one recipe step."""

    connector: str
    action: str
    resource_type: str
    permissions: frozenset[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "permissions",
            frozenset(value.strip() for value in self.permissions if value.strip()),
        )


@dataclass(frozen=True, slots=True)
class CapabilityDecision:
    """Safe, machine-readable result of a capability evaluation."""

    allowed: bool
    code: str
    reason: str
    capability: ConnectorCapability | None = None
    missing_permissions: frozenset[str] = field(default_factory=frozenset)
    undeclared_permissions: frozenset[str] = field(default_factory=frozenset)
    requires_approval: bool = False
    irreversible: bool = False


@dataclass(frozen=True, slots=True)
class ConnectorManifest:
    """A strict declaration of what a connector can do before credentials are used."""

    name: str
    version: str
    protocol_versions: frozenset[str]
    resource_types: frozenset[str]
    capabilities: tuple[ConnectorCapability, ...]
    authentication_methods: frozenset[str]
    minimum_permissions: frozenset[str]
    supports_polling: bool
    supports_webhooks: bool
    rate_limit_strategy: str
    retry_policy: RetryPolicy
    sensitive_fields: frozenset[str]
    data_classes: frozenset[str]
    default_redaction: RedactionMode
    deletion_behavior: str
    recovery_supported: bool
    fixtures: frozenset[str]
    conformance_tests: frozenset[str]
    schema_version: str = MANIFEST_SCHEMA_VERSION

    def __post_init__(self) -> None:
        normalized_sets = {
            "protocol_versions": self.protocol_versions,
            "resource_types": self.resource_types,
            "authentication_methods": self.authentication_methods,
            "minimum_permissions": self.minimum_permissions,
            "sensitive_fields": self.sensitive_fields,
            "data_classes": self.data_classes,
            "fixtures": self.fixtures,
            "conformance_tests": self.conformance_tests,
        }
        for attribute, values in normalized_sets.items():
            object.__setattr__(
                self,
                attribute,
                frozenset(value.strip() for value in values if value.strip()),
            )

        name = self.name.strip()
        version = self.version.strip()
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "version", version)
        object.__setattr__(self, "capabilities", tuple(self.capabilities))

        if self.schema_version != MANIFEST_SCHEMA_VERSION:
            raise CapabilityContractError(
                f"unsupported manifest schema version: {self.schema_version!r}"
            )
        if not _NAME_PATTERN.fullmatch(name):
            raise CapabilityContractError(f"invalid connector name: {name!r}")
        if not _VERSION_PATTERN.fullmatch(version):
            raise CapabilityContractError(f"invalid connector version: {version!r}")
        if not self.protocol_versions:
            raise CapabilityContractError("protocol_versions cannot be empty")
        if not self.resource_types:
            raise CapabilityContractError("resource_types cannot be empty")
        if not self.authentication_methods:
            raise CapabilityContractError("authentication_methods cannot be empty")
        if self.rate_limit_strategy not in {"none", "provider", "fixed"}:
            raise CapabilityContractError(
                f"unsupported rate limit strategy: {self.rate_limit_strategy!r}"
            )
        if self.deletion_behavior not in {
            "none",
            "soft_delete",
            "hard_delete",
            "provider_defined",
        }:
            raise CapabilityContractError(
                f"unsupported deletion behavior: {self.deletion_behavior!r}"
            )

        action_names: set[str] = set()
        for capability in self.capabilities:
            if capability.action in action_names:
                raise CapabilityContractError(
                    f"capability action {capability.action!r} is declared more than once"
                )
            action_names.add(capability.action)

            undeclared_resources = capability.resource_types - self.resource_types
            if undeclared_resources:
                raise CapabilityContractError(
                    f"{capability.action!r} uses undeclared resource types: "
                    f"{sorted(undeclared_resources)}"
                )

        has_delete = any(
            capability.operation is ConnectorOperation.DELETE
            for capability in self.capabilities
        )
        if has_delete and self.deletion_behavior == "none":
            raise CapabilityContractError(
                "delete capabilities require an explicit deletion behavior"
            )

    @property
    def write_capabilities(self) -> tuple[ConnectorCapability, ...]:
        return tuple(
            capability
            for capability in self.capabilities
            if capability.operation.is_write
        )

    def is_protocol_compatible(self, runtime_protocol: str = PROTOCOL_VERSION) -> bool:
        return runtime_protocol in self.protocol_versions

    def capability_for(
        self,
        *,
        action: str,
        resource_type: str,
    ) -> ConnectorCapability | None:
        return next(
            (
                capability
                for capability in self.capabilities
                if capability.supports(action=action, resource_type=resource_type)
            ),
            None,
        )

    def evaluate_action(
        self,
        action: ProposedAction,
        granted_permissions: Iterable[str],
        *,
        runtime_protocol: str = PROTOCOL_VERSION,
    ) -> CapabilityDecision:
        """Refuse actions absent from the manifest or current credential scope."""

        if action.target.connector != self.name:
            return CapabilityDecision(
                allowed=False,
                code="connector_mismatch",
                reason="the action target does not match the connector manifest",
            )
        if not self.is_protocol_compatible(runtime_protocol):
            return CapabilityDecision(
                allowed=False,
                code="protocol_incompatible",
                reason="the connector does not declare the runtime protocol",
            )

        capability = self.capability_for(
            action=action.action,
            resource_type=action.target.resource_type,
        )
        if capability is None:
            return CapabilityDecision(
                allowed=False,
                code="undeclared_action",
                reason="the connector manifest does not declare this action and resource type",
            )

        granted = frozenset(granted_permissions)
        required = self.minimum_permissions | capability.required_permissions
        missing = required - granted
        if missing:
            return CapabilityDecision(
                allowed=False,
                code="missing_permissions",
                reason="the active credential lacks declared minimum permissions",
                capability=capability,
                missing_permissions=missing,
                requires_approval=action.requires_approval or capability.requires_approval,
                irreversible=capability.irreversible,
            )

        return CapabilityDecision(
            allowed=True,
            code="allowed",
            reason="the action and permissions are declared by the connector manifest",
            capability=capability,
            requires_approval=action.requires_approval or capability.requires_approval,
            irreversible=capability.irreversible,
        )

    def evaluate_requirement(
        self,
        requirement: CapabilityRequirement,
        granted_permissions: Iterable[str],
        *,
        runtime_protocol: str = PROTOCOL_VERSION,
    ) -> CapabilityDecision:
        """Compare a recipe requirement with manifest and active credential authority."""

        if requirement.connector != self.name:
            return CapabilityDecision(
                allowed=False,
                code="connector_mismatch",
                reason="the recipe requirement targets another connector",
            )
        if not self.is_protocol_compatible(runtime_protocol):
            return CapabilityDecision(
                allowed=False,
                code="protocol_incompatible",
                reason="the connector does not declare the runtime protocol",
            )

        capability = self.capability_for(
            action=requirement.action,
            resource_type=requirement.resource_type,
        )
        if capability is None:
            return CapabilityDecision(
                allowed=False,
                code="undeclared_action",
                reason="the recipe requests an undeclared action or resource type",
            )

        declared_permissions = self.minimum_permissions | capability.required_permissions
        undeclared = requirement.permissions - declared_permissions
        if undeclared:
            return CapabilityDecision(
                allowed=False,
                code="undeclared_recipe_permissions",
                reason="the recipe requests permissions absent from the capability declaration",
                capability=capability,
                undeclared_permissions=undeclared,
                requires_approval=capability.requires_approval,
                irreversible=capability.irreversible,
            )

        missing = declared_permissions - frozenset(granted_permissions)
        if missing:
            return CapabilityDecision(
                allowed=False,
                code="missing_permissions",
                reason="the active credential lacks permissions required by the recipe",
                capability=capability,
                missing_permissions=missing,
                requires_approval=capability.requires_approval,
                irreversible=capability.irreversible,
            )

        return CapabilityDecision(
            allowed=True,
            code="allowed",
            reason="the recipe requirement fits declared and granted authority",
            capability=capability,
            requires_approval=capability.requires_approval,
            irreversible=capability.irreversible,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "name": self.name,
            "version": self.version,
            "protocol_versions": sorted(self.protocol_versions),
            "resource_types": sorted(self.resource_types),
            "capabilities": [capability.to_dict() for capability in self.capabilities],
            "authentication": {
                "methods": sorted(self.authentication_methods),
                "minimum_permissions": sorted(self.minimum_permissions),
            },
            "delivery": {
                "polling": self.supports_polling,
                "webhooks": self.supports_webhooks,
            },
            "rate_limit": {
                "strategy": self.rate_limit_strategy,
                "retry": {
                    "strategy": self.retry_policy.strategy,
                    "max_attempts": self.retry_policy.max_attempts,
                    "honors_retry_after": self.retry_policy.honors_retry_after,
                },
            },
            "sensitivity": {
                "sensitive_fields": sorted(self.sensitive_fields),
                "data_classes": sorted(self.data_classes),
                "default_redaction": self.default_redaction.value,
            },
            "deletion": {
                "behavior": self.deletion_behavior,
                "recovery_supported": self.recovery_supported,
            },
            "conformance": {
                "fixtures": sorted(self.fixtures),
                "tests": sorted(self.conformance_tests),
            },
        }

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> ConnectorManifest:
        """Build and validate a manifest loaded from JSON or TOML."""

        try:
            authentication = value["authentication"]
            delivery = value["delivery"]
            rate_limit = value["rate_limit"]
            retry = rate_limit["retry"]
            sensitivity = value["sensitivity"]
            deletion = value["deletion"]
            conformance = value["conformance"]

            capabilities = tuple(
                ConnectorCapability(
                    action=item["action"],
                    operation=ConnectorOperation(item["operation"]),
                    resource_types=frozenset(item["resource_types"]),
                    required_permissions=frozenset(item["required_permissions"]),
                    idempotent=item["idempotent"],
                    conditional_updates=item["conditional_updates"],
                    irreversible=item["irreversible"],
                    requires_approval=item["requires_approval"],
                )
                for item in value["capabilities"]
            )
            return cls(
                schema_version=value["schema_version"],
                name=value["name"],
                version=value["version"],
                protocol_versions=frozenset(value["protocol_versions"]),
                resource_types=frozenset(value["resource_types"]),
                capabilities=capabilities,
                authentication_methods=frozenset(authentication["methods"]),
                minimum_permissions=frozenset(authentication["minimum_permissions"]),
                supports_polling=delivery["polling"],
                supports_webhooks=delivery["webhooks"],
                rate_limit_strategy=rate_limit["strategy"],
                retry_policy=RetryPolicy(
                    strategy=retry["strategy"],
                    max_attempts=retry["max_attempts"],
                    honors_retry_after=retry["honors_retry_after"],
                ),
                sensitive_fields=frozenset(sensitivity["sensitive_fields"]),
                data_classes=frozenset(sensitivity["data_classes"]),
                default_redaction=RedactionMode(sensitivity["default_redaction"]),
                deletion_behavior=deletion["behavior"],
                recovery_supported=deletion["recovery_supported"],
                fixtures=frozenset(conformance["fixtures"]),
                conformance_tests=frozenset(conformance["tests"]),
            )
        except (KeyError, TypeError, ValueError) as exc:
            if isinstance(exc, CapabilityContractError):
                raise
            raise CapabilityContractError("invalid connector manifest structure") from exc
