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

    assert records[0].status is ActionStatus.PLANNED
    assert connector.actions == []


def test_unapproved_action_waits() -> None:
    connector = RecordingConnector(name="notion")
    engine = GrimoireEngine(connectors={"notion": connector})
    action = make_action()

    records = engine.run(make_event(), [action], dry_run=False)

    assert records[0].status is ActionStatus.AWAITING_APPROVAL
    assert connector.actions == []


def test_approved_action_executes() -> None:
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
