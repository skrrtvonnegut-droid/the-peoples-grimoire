"""Cross-document bundle validation for Grimoire trust manifests."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from ._validation_common import ValidationFailure, ValidationResult, _load_document
from ._validation_document import validate_document


def _candidate_documents(root: Path) -> list[Path]:
    candidates: list[Path] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in {".json", ".yaml", ".yml"}:
            continue
        try:
            document = _load_document(path)
        except ValidationFailure:
            try:
                raw_text = path.read_text(encoding="utf-8")
            except OSError:
                continue
            if "grimoire." in raw_text and "kind" in raw_text:
                candidates.append(path)
            continue

        kind = document.get("kind")
        if isinstance(kind, str) and kind.startswith("grimoire."):
            candidates.append(path)
    return candidates


def _bundle_reference_errors(documents: Mapping[Path, Mapping[str, Any]]) -> dict[Path, list[str]]:
    additions: dict[Path, list[str]] = defaultdict(list)
    connector_by_id: dict[str, tuple[Path, Mapping[str, Any]]] = {}

    for path, document in documents.items():
        if document.get("kind") != "grimoire.connector":
            continue
        connector_id = document.get("id")
        if not isinstance(connector_id, str):
            continue
        if connector_id in connector_by_id:
            first_path, _ = connector_by_id[connector_id]
            additions[path].append(
                f"$.id duplicates connector manifest {connector_id!r} from {first_path.name}"
            )
            additions[first_path].append(
                f"$.id duplicates connector manifest {connector_id!r} from {path.name}"
            )
        else:
            connector_by_id[connector_id] = (path, document)

    for path, document in documents.items():
        if document.get("kind") != "grimoire.instance":
            continue

        policy = document.get("policy")
        approvals = policy.get("approvals", {}) if isinstance(policy, Mapping) else {}
        systems = document.get("systems")
        if not isinstance(systems, Mapping):
            continue

        for alias, binding in systems.items():
            if not isinstance(binding, Mapping):
                continue
            manifest_id = binding.get("connector_manifest")
            manifest_entry = (
                connector_by_id.get(manifest_id) if isinstance(manifest_id, str) else None
            )
            if manifest_entry is None:
                additions[path].append(
                    f"$.systems.{alias}.connector_manifest references {manifest_id!r}, "
                    "which is not present in this validation bundle"
                )
                continue

            _, connector = manifest_entry
            capabilities = {
                item.get("id"): item
                for item in connector.get("capabilities", [])
                if isinstance(item, Mapping) and isinstance(item.get("id"), str)
            }
            for index, capability_id in enumerate(binding.get("enabled_capabilities", [])):
                capability = capabilities.get(capability_id)
                if capability is None:
                    additions[path].append(
                        f"$.systems.{alias}.enabled_capabilities[{index}] references "
                        f"unknown capability {capability_id!r} in {manifest_id!r}"
                    )
                    continue
                _check_instance_effect_policy(
                    additions[path],
                    alias=str(alias),
                    capability_id=str(capability_id),
                    effect=capability.get("effect"),
                    approvals=approvals,
                )

    return additions


def _check_instance_effect_policy(
    errors: list[str],
    *,
    alias: str,
    capability_id: str,
    effect: Any,
    approvals: Any,
) -> None:
    if not isinstance(approvals, Mapping):
        return

    policy_field: str | None = None
    if effect == "write":
        policy_field = "write"
    elif effect == "destructive":
        policy_field = "delete"
    elif effect == "audience-changing":
        policy_field = "publish"
    elif effect == "administrative":
        policy_field = "write"

    if policy_field and approvals.get(policy_field) == "forbidden":
        errors.append(
            f"$.systems.{alias}.enabled_capabilities enables {capability_id!r} with "
            f"effect {effect!r}, but $.policy.approvals.{policy_field} is forbidden"
        )


def validate_path(path: Path) -> list[ValidationResult]:
    """Validate one manifest or a complete manifest bundle."""

    path = path.expanduser().resolve()
    if not path.exists():
        return [ValidationResult(path=path, errors=("path does not exist",))]
    if path.is_file():
        return [validate_document(path)]

    candidates = _candidate_documents(path)
    if not candidates:
        return [
            ValidationResult(
                path=path,
                errors=("directory contains no typed Grimoire YAML or JSON documents",),
            )
        ]

    results = {candidate: validate_document(candidate) for candidate in candidates}
    documents: dict[Path, Mapping[str, Any]] = {}
    for candidate, result in results.items():
        load_failed = any(
            error.startswith("cannot parse") or error.startswith("cannot read")
            for error in result.errors
        )
        if load_failed:
            continue
        try:
            documents[candidate] = _load_document(candidate)
        except ValidationFailure:
            continue

    additions = _bundle_reference_errors(documents)
    return [
        ValidationResult(
            path=candidate,
            errors=tuple(
                dict.fromkeys((*results[candidate].errors, *additions.get(candidate, [])))
            ),
        )
        for candidate in candidates
    ]
