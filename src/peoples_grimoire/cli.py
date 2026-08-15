"""Command-line interface for the pre-alpha reference runtime."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from datetime import UTC, datetime
from pathlib import Path

from .connectors.memory import RecordingConnector
from .engine import GrimoireEngine
from .models import EventKind, GrimoireEvent, ProposedAction, ResourceRef
from .validation import validate_path


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


def _display_path(path: Path) -> Path:
    try:
        return path.relative_to(Path.cwd().resolve())
    except ValueError:
        return path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="grimoire",
        description="Inspect the pre-alpha runtime and validate Grimoire trust manifests.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    demo = subparsers.add_parser("demo", help="print a sanitized Notion/GitHub plan")
    demo.add_argument(
        "--apply",
        action="store_true",
        help="execute against an in-memory connector after explicit approval",
    )

    validate = subparsers.add_parser(
        "validate",
        help="validate one trust manifest or a bundle of typed manifests",
    )
    validate.add_argument("path", type=Path, help="manifest file or directory to validate")
    validate.add_argument(
        "--quiet",
        action="store_true",
        help="print only failures and the final summary",
    )
    return parser


def _run_demo(*, apply: bool) -> int:
    event, action = build_demo()
    connector = RecordingConnector(name="notion")
    engine = GrimoireEngine(connectors={"notion": connector})

    approved = frozenset({action.action_id}) if apply else frozenset()
    records = engine.run(
        event,
        [action],
        dry_run=not apply,
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


def _run_validate(path: Path, *, quiet: bool) -> int:
    results = validate_path(path)
    failures = 0

    for result in results:
        if result.errors:
            failures += 1
            print(f"FAIL {_display_path(result.path)}")
            for error in result.errors:
                print(f"  - {error}")
        elif not quiet:
            print(f"OK  {_display_path(result.path)}")

    print(f"Validated {len(results)} Grimoire document(s); {failures} failure(s).")
    return 1 if failures else 0


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.command == "demo":
        return _run_demo(apply=args.apply)
    if args.command == "validate":
        return _run_validate(args.path, quiet=args.quiet)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
