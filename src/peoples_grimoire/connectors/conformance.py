"""Reusable connector manifest and implementation conformance checks."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from peoples_grimoire.models import ProposedAction

from .base import Connector, ExecutionResult
from .capabilities import PROTOCOL_VERSION, ConnectorManifest


@dataclass(frozen=True, slots=True)
class ConformanceReport:
    """A compact report suitable for tests and connector CI."""

    passed: bool
    findings: tuple[str, ...]

    def require(self) -> None:
        if not self.passed:
            raise AssertionError("; ".join(self.findings))


@dataclass(frozen=True, slots=True)
class ConnectorBehaviorCase:
    """One synthetic action used to verify manifest enforcement and connector shape."""

    action: ProposedAction
    expect_allowed: bool
    execute: bool = False


def check_manifest_conformance(
    manifest: ConnectorManifest,
    *,
    runtime_protocol: str = PROTOCOL_VERSION,
) -> ConformanceReport:
    findings: list[str] = []

    if not manifest.is_protocol_compatible(runtime_protocol):
        findings.append(f"protocol {runtime_protocol!r} is not declared")
    if not manifest.fixtures:
        findings.append("no synthetic fixture coverage is declared")
    if not manifest.conformance_tests:
        findings.append("no conformance tests are declared")
    if manifest.write_capabilities and not manifest.sensitive_fields:
        findings.append("write-capable connectors must declare sensitive fields")

    return ConformanceReport(passed=not findings, findings=tuple(findings))


def check_connector_conformance(
    connector: Connector,
    *,
    runtime_protocol: str = PROTOCOL_VERSION,
) -> ConformanceReport:
    findings = list(
        check_manifest_conformance(
            connector.manifest,
            runtime_protocol=runtime_protocol,
        ).findings
    )

    if connector.name != connector.manifest.name:
        findings.append("connector name does not match manifest name")
    if not callable(getattr(connector, "execute", None)):
        findings.append("connector execute method is missing")
    if not isinstance(connector.granted_permissions, frozenset):
        findings.append("granted_permissions must be a frozenset")

    return ConformanceReport(passed=not findings, findings=tuple(findings))


def check_connector_behavior(
    connector: Connector,
    cases: Iterable[ConnectorBehaviorCase],
) -> ConformanceReport:
    """Exercise declared and denied actions against a connector's synthetic transport."""

    findings = list(check_connector_conformance(connector).findings)

    for index, case in enumerate(cases):
        decision = connector.manifest.evaluate_action(
            case.action,
            connector.granted_permissions,
        )
        if decision.allowed is not case.expect_allowed:
            findings.append(
                f"case {index}: expected allowed={case.expect_allowed}, "
                f"received {decision.code!r}"
            )
            continue

        if case.execute and decision.allowed:
            try:
                result = connector.execute(case.action)
            except Exception as exc:
                findings.append(
                    f"case {index}: synthetic execution raised {type(exc).__name__}"
                )
            else:
                if not isinstance(result, ExecutionResult):
                    findings.append(
                        f"case {index}: execute must return ExecutionResult"
                    )

    return ConformanceReport(passed=not findings, findings=tuple(findings))


def assert_connector_conforms(connector: Connector) -> None:
    check_connector_conformance(connector).require()
