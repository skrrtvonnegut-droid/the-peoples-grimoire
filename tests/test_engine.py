import json
from datetime import UTC, datetime

from peoples_grimoire.connectors.memory import RecordingConnector
from peoples_grimoire.engine import GrimoireEngine
from peoples_grimoire.models import (
    ActionStatus,
    EventKind,
    GrimoireEvent,
    ProposedAction,
    ResourceRef,
)
from peoples_grimoire.observability import StructuredLogger
from peoples_grimoire.redaction import Redactor


def make_event() -> GrimoireEvent:
    return GrimoireEvent(
        source=ResourceRef("github", "issue", "example/repository#1"),
        kind=EventKind.UPDATED,
        occurred_at=datetime(2026, 8, 15, tzinfo=UTC),
        payload={"state": "closed"},
    )


def make_action(*, requires_approval: bool = True) -> ProposedAction:
    return ProposedAction(
        target=ResourceRef("notion", "page", "example-page"),
        action="update_properties",
        changes={"Status": "Done"},
        reason="Reflect the linked issue state.",
        requires_approval=requires_approval,
    )


def test_event_id_is_deterministic() -> None:
    assert make_event().event_id == make_event().event_id


def test_dry_run_never_executes_connector() -> None:
    connector = RecordingConnector(name="notion")
    engine = GrimoireEngine(connectors={"notion": connector})
    action = make_action(requires_approval=False)

    records = engine.run(make_event(), [action], dry_run=True)

    assert records[0].status is ActionStatus.AWAITING_APPROVAL
    assert connector.actions == []


def test_unapproved_action_waits() -> None:
    connector = RecordingConnector(name="notion")
    engine = GrimoireEngine(connectors={"notion": connector})
    action = make_action()

    records = engine.run(make_event(), [action], dry_run=False)

    assert records[0].status is ActionStatus.AWAITING_APPROVAL
    assert connector.actions == []


def test_approved_action_executes_and_private_result_ids_are_fingerprinted() -> None:
    connector = RecordingConnector(name="notion")
    engine = GrimoireEngine(connectors={"notion": connector})
    action = make_action()

    records = engine.run(
        make_event(),
        [action],
        dry_run=False,
        approved_action_ids=frozenset({action.action_id}),
    )

    assert records[0].status is ActionStatus.EXECUTED
    assert connector.actions == [action]
    assert records[0].detail["external_id_fingerprint"].startswith("fp_")
    assert "example-page" not in str(records[0].detail)


def test_undeclared_action_is_refused_before_connector_execution() -> None:
    connector = RecordingConnector(name="notion")
    engine = GrimoireEngine(connectors={"notion": connector})
    action = ProposedAction(
        target=ResourceRef("notion", "page", "example-page"),
        action="delete_everything",
        changes={},
        reason="Synthetic negative test.",
        requires_approval=False,
    )

    records = engine.run(make_event(), [action], dry_run=False)

    assert records[0].status is ActionStatus.FAILED
    assert records[0].detail["error_code"] == "undeclared_action"
    assert connector.actions == []


def test_engine_emits_correlated_structured_record() -> None:
    lines: list[str] = []
    connector = RecordingConnector(name="notion")
    logger = StructuredLogger(
        sink=lines.append,
        redactor=Redactor(fingerprint_key=b"x" * 32),
    )
    engine = GrimoireEngine(
        connectors={"notion": connector},
        logger=logger,
        redactor=logger.redactor,
    )
    action = make_action()

    engine.run(
        make_event(),
        [action],
        dry_run=True,
        correlation_id="corr_test",
        recipe_id="rcp_test",
    )

    record = json.loads(lines[0])
    assert record["correlation_id"] == "corr_test"
    assert record["event_id"] == make_event().event_id
    assert record["action_id"] == action.action_id
    assert record["recipe_id"] == "rcp_test"
    assert record["connector_id"] == "notion"
    assert record["fields"]["status"] == "awaiting_approval"


def test_connector_exception_is_replaced_by_safe_diagnostic() -> None:
    sensitive_message = "Bearer " + "oauth-access-token-abcdefghijklmnopqrstuvwxyz"

    class FailingConnector(RecordingConnector):
        def execute(self, action: ProposedAction):
            raise RuntimeError(f"provider returned {sensitive_message}")

    connector = FailingConnector(name="notion")
    engine = GrimoireEngine(
        connectors={"notion": connector},
        redactor=Redactor(fingerprint_key=b"x" * 32),
    )
    action = make_action()

    records = engine.run(
        make_event(),
        [action],
        dry_run=False,
        approved_action_ids=frozenset({action.action_id}),
        correlation_id="corr_test",
    )

    serialized = json.dumps(records[0].detail)
    assert records[0].status is ActionStatus.FAILED
    assert records[0].detail["error_code"] == "operation_failed"
    assert records[0].detail["diagnostic_id"].startswith("diag_")
    assert sensitive_message not in serialized
