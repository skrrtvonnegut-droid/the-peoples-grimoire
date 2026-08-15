"""Connector contracts and development helpers."""

from .base import Connector, ConnectorExecutionError, ExecutionResult
from .capabilities import (
    MANIFEST_SCHEMA_VERSION,
    PROTOCOL_VERSION,
    CapabilityContractError,
    CapabilityDecision,
    CapabilityRequirement,
    ConnectorCapability,
    ConnectorManifest,
    ConnectorOperation,
    RedactionMode,
    RetryPolicy,
)
from .conformance import (
    ConformanceReport,
    ConnectorBehaviorCase,
    assert_connector_conforms,
    check_connector_behavior,
    check_connector_conformance,
    check_manifest_conformance,
)
from .memory import RecordingConnector

__all__ = [
    "MANIFEST_SCHEMA_VERSION",
    "PROTOCOL_VERSION",
    "CapabilityContractError",
    "CapabilityDecision",
    "CapabilityRequirement",
    "ConformanceReport",
    "ConnectorBehaviorCase",
    "Connector",
    "ConnectorCapability",
    "ConnectorExecutionError",
    "ConnectorManifest",
    "ConnectorOperation",
    "ExecutionResult",
    "RecordingConnector",
    "RedactionMode",
    "RetryPolicy",
    "assert_connector_conforms",
    "check_connector_behavior",
    "check_connector_conformance",
    "check_manifest_conformance",
]
