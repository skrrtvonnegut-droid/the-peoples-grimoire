"""Small demonstration CLI for the pre-alpha reference runtime."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from datetime import UTC, datetime

from .connectors.memory import RecordingConnector
from .engine import GrimoireEngine
from .models import EventKind, GrimoireEvent, ProposedAction, ResourceRef


def build_demo() -> tuple[GrimoireEvent, ProposedAction]:
    event = GrimoireEvent(
        source=ResourceRef(
            connector="github",
            resource_type="issue",
            external_id="example/repository#42",
            url="https://github.com/example/repository/issues/42",
        ),
        kind=EventKind.UPDATED,
        occurred_at=datetime.now(UTC),
        payload={"title": "Design the canonical event envelope", "state": "open"},
        provenance={"fixture": "sanitized-demo"},
    )
    action = ProposedAction(
        target=ResourceRef(
            connector="notion",
            resource_type="page",
            external_id="example-page",
        ),
        action="update_properties",
        changes={"Status": "In progress", "Source": event.source.url},
        reason="Keep the linked project memory aligned with the GitHub issue.",
        requires_approval=True,
    )
    return event, action


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="grimoire")
    subparsers = parser.add_subparsers(dest="command", required=True)

    demo = subparsers.add_parser("demo", help="print a sanitized Notion/GitHub plan")
    demo.add_argument(
        "--apply",
        action="store_true",
        help="execute against an in-memory connector after explicit approval",
    )

    args = parser.parse_args(argv)
    event, action = build_demo()
    connector = RecordingConnector(name="notion")
    engine = GrimoireEngine(connectors={"notion": connector})

    approved = frozenset({action.action_id}) if args.apply else frozenset()
    records = engine.run(
        event,
        [action],
        dry_run=not args.apply,
        approved_action_ids=approved,
    )
    print(
        json.dumps(
            {
                "event": event.to_dict(),
                "records": [record.to_dict() for record in records],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
