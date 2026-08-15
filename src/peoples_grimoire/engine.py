"""Plan/apply execution boundary for connector actions."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime

from .connectors.base import Connector, ConnectorExecutionError
from .models import ActionRecord, ActionStatus, GrimoireEvent, ProposedAction


@dataclass(slots=True)
class InMemoryLedger:
    """Small append-only ledger used until a durable store is introduced."""

    records: list[ActionRecord] = field(default_factory=list)

    def append(self, record: ActionRecord) -> None:
        self.records.append(record)


@dataclass(slots=True)
class GrimoireEngine:
    """Execute explicit plans through registered connectors.

    Planning and policy evaluation intentionally remain separate. This boundary
    makes dry-runs, approvals, and later durable audit storage possible without
    hiding writes inside connector-specific code.
    """

    connectors: Mapping[str, Connector]
    ledger: InMemoryLedger = field(default_factory=InMemoryLedger)

    def run(
        self,
        event: GrimoireEvent,
        actions: Iterable[ProposedAction],
        *,
        dry_run: bool = True,
        approved_action_ids: frozenset[str] | None = None,
    ) -> list[ActionRecord]:
        records: list[ActionRecord] = []
        approved_action_ids = approved_action_ids or frozenset()

        for action in actions:
            status = ActionStatus.PLANNED
            detail: dict[str, object] = {"dry_run": dry_run}

            if action.requires_approval and action.action_id not in approved_action_ids:
                status = ActionStatus.AWAITING_APPROVAL
                detail["reason"] = "explicit approval required"
            elif not dry_run:
                connector = self.connectors.get(action.target.connector)
                if connector is None:
                    status = ActionStatus.FAILED
                    detail["error"] = f"no connector registered for {action.target.connector!r}"
                else:
                    try:
                        result = connector.execute(action)
                    except ConnectorExecutionError as exc:
                        status = ActionStatus.FAILED
                        detail["error"] = str(exc)
                    else:
                        status = ActionStatus.EXECUTED
                        detail.update(result.detail)
                        if result.external_id is not None:
                            detail["external_id"] = result.external_id
                        if result.url is not None:
                            detail["url"] = result.url

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

        return records
