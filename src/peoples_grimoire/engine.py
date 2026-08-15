"""Plan/apply execution boundary for connector actions."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime

from .connectors.base import Connector
from .engine_types import ConnectorDecisionContext
from .models import ActionRecord, ActionStatus, GrimoireEvent, ProposedAction
from .observability import LogContext, StructuredLogger, new_correlation_id
from .redaction import Redactor, safe_exception_summary


@dataclass(slots=True)
class InMemoryLedger:
    """Small append-only ledger used until a durable store is introduced."""

    records: list[ActionRecord] = field(default_factory=list)

    def append(self, record: ActionRecord) -> None:
        self.records.append(record)


@dataclass(slots=True)
class GrimoireEngine:
    """Execute explicit plans through capability-declaring connectors."""

    connectors: Mapping[str, Connector]
    ledger: InMemoryLedger = field(default_factory=InMemoryLedger)
    logger: StructuredLogger | None = None
    redactor: Redactor = field(default_factory=Redactor)

    def run(
        self,
        event: GrimoireEvent,
        actions: Iterable[ProposedAction],
        *,
        dry_run: bool = True,
        approved_action_ids: frozenset[str] | None = None,
        correlation_id: str | None = None,
        recipe_id: str | None = None,
        recipe_sensitive_fields: Iterable[str] = (),
    ) -> list[ActionRecord]:
        records: list[ActionRecord] = []
        approved_action_ids = approved_action_ids or frozenset()
        correlation_id = correlation_id or new_correlation_id()
        recipe_sensitive_fields = frozenset(recipe_sensitive_fields)

        for action in actions:
            status = ActionStatus.PLANNED
            detail: dict[str, object] = {"dry_run": dry_run}
            connector = self.connectors.get(action.target.connector)
            decision_context = ConnectorDecisionContext()

            if connector is None:
                status = ActionStatus.FAILED
                detail["error_code"] = "connector_not_registered"
            else:
                decision = connector.manifest.evaluate_action(
                    action,
                    connector.granted_permissions,
                )
                decision_context = ConnectorDecisionContext.from_decision(decision)

                if not decision.allowed:
                    status = ActionStatus.FAILED
                    detail["error_code"] = decision.code
                    if decision.missing_permissions:
                        detail["missing_permissions"] = sorted(decision.missing_permissions)
                    if decision.undeclared_permissions:
                        detail["undeclared_permissions"] = sorted(
                            decision.undeclared_permissions
                        )
                elif (
                    decision.requires_approval
                    and action.action_id not in approved_action_ids
                ):
                    status = ActionStatus.AWAITING_APPROVAL
                    detail["reason"] = "explicit approval required"
                elif not dry_run:
                    try:
                        result = connector.execute(action)
                    except Exception as exc:
                        status = ActionStatus.FAILED
                        detail.update(
                            safe_exception_summary(
                                exc,
                                correlation_id=correlation_id,
                                redactor=self.redactor,
                            )
                        )
                    else:
                        status = ActionStatus.EXECUTED
                        detail["result"] = self.redactor.sanitize_connector_payload(
                            result.detail,
                            safe_fields=result.safe_detail_fields,
                            sensitive_fields=(
                                connector.manifest.sensitive_fields
                                | recipe_sensitive_fields
                            ),
                        )
                        if result.external_id is not None:
                            detail["external_id_fingerprint"] = (
                                self.redactor.private_fingerprint(result.external_id)
                            )
                        if result.url is not None:
                            detail["url_fingerprint"] = (
                                self.redactor.private_fingerprint(result.url)
                            )

            record = ActionRecord(
                event_id=event.event_id or "unknown",
                action_id=action.action_id or "unknown",
                target=action.target,
                status=status,
                recorded_at=datetime.now(UTC),
                detail=detail,
            )
            self.ledger.append(record)
            records.append(record)

            if self.logger is not None:
                log_fields: dict[str, object] = {
                    "status": status.value,
                    "dry_run": dry_run,
                    "resource_type": action.target.resource_type,
                    "operation": decision_context.operation,
                    "requires_approval": decision_context.requires_approval,
                    "irreversible": decision_context.irreversible,
                }
                if "error_code" in detail:
                    log_fields["error_code"] = detail["error_code"]
                if "error_type" in detail:
                    log_fields["error_type"] = detail["error_type"]
                if "diagnostic_id" in detail:
                    log_fields["diagnostic_id"] = detail["diagnostic_id"]
                if "missing_permissions" in detail:
                    log_fields["missing_permissions"] = detail["missing_permissions"]

                self.logger.emit(
                    level="error" if status is ActionStatus.FAILED else "info",
                    event="action.recorded",
                    context=LogContext(
                        correlation_id=correlation_id,
                        connector_id=action.target.connector,
                        event_id=event.event_id,
                        action_id=action.action_id,
                        recipe_id=recipe_id,
                    ),
                    fields=log_fields,
                    sensitive_fields=(
                        (
                            connector.manifest.sensitive_fields
                            if connector is not None
                            else frozenset()
                        )
                        | recipe_sensitive_fields
                    ),
                )

        return records
