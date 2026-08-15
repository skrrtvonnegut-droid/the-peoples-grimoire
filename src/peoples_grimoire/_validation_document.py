"""Single-document validation for Grimoire trust manifests."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

from ._validation_common import (
    SCHEMA_BY_KIND,
    ValidationFailure,
    ValidationResult,
    _format_json_path,
    _load_document,
    _load_schema,
    _scan_for_inline_secrets,
)


def validate_document(path: Path) -> ValidationResult:
    """Validate one typed Grimoire manifest without resolving bundle references."""

    errors: list[str] = []

    try:
        document = _load_document(path)
    except ValidationFailure as exc:
        return ValidationResult(path=path, errors=(str(exc),))

    errors.extend(_scan_for_inline_secrets(document))

    kind = document.get("kind")
    if not isinstance(kind, str):
        errors.append("$.kind is required and must be a string")
        return ValidationResult(path=path, errors=tuple(errors))

    schema_filename = SCHEMA_BY_KIND.get(kind)
    if schema_filename is None:
        supported = ", ".join(sorted(SCHEMA_BY_KIND))
        errors.append(f"$.kind {kind!r} is unsupported; expected one of: {supported}")
        return ValidationResult(path=path, errors=tuple(errors))

    schema = _load_schema(schema_filename)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())

    for error in sorted(validator.iter_errors(document), key=lambda item: list(item.path)):
        errors.append(f"{_format_json_path(error.path)}: {error.message}")

    errors.extend(_document_semantic_errors(document))
    return ValidationResult(path=path, errors=tuple(dict.fromkeys(errors)))


def _document_semantic_errors(document: Mapping[str, Any]) -> list[str]:
    kind = document.get("kind")
    errors: list[str] = []

    if kind == "grimoire.connector":
        errors.extend(
            _duplicate_id_errors(
                document.get("resource_types"),
                "id",
                "$.resource_types",
            )
        )
        errors.extend(
            _duplicate_id_errors(
                document.get("capabilities"),
                "id",
                "$.capabilities",
            )
        )

        resource_ids = {
            item.get("id")
            for item in document.get("resource_types", [])
            if isinstance(item, Mapping) and isinstance(item.get("id"), str)
        }
        for index, capability in enumerate(document.get("capabilities", [])):
            if not isinstance(capability, Mapping):
                continue
            for resource_type in capability.get("resource_types", []):
                if resource_type not in resource_ids:
                    errors.append(
                        f"$.capabilities[{index}].resource_types references {resource_type!r}, "
                        "which is not declared in $.resource_types"
                    )

    elif kind == "grimoire.artifact":
        errors.extend(
            _duplicate_id_errors(
                document.get("representations"),
                "id",
                "$.representations",
            )
        )
        errors.extend(
            _duplicate_id_errors(
                document.get("authority"),
                "concern",
                "$.authority",
            )
        )

        representation_ids = {
            item.get("id")
            for item in document.get("representations", [])
            if isinstance(item, Mapping) and isinstance(item.get("id"), str)
        }
        for index, rule in enumerate(document.get("authority", [])):
            if not isinstance(rule, Mapping):
                continue
            representation = rule.get("representation")
            if isinstance(representation, str) and representation not in representation_ids:
                errors.append(
                    f"$.authority[{index}].representation references {representation!r}, "
                    "which is not declared in $.representations"
                )

    return errors


def _duplicate_id_errors(items: Any, field: str, json_path: str) -> list[str]:
    if not isinstance(items, list):
        return []

    positions: dict[str, list[int]] = defaultdict(list)
    for index, item in enumerate(items):
        if isinstance(item, Mapping) and isinstance(item.get(field), str):
            positions[item[field]].append(index)

    return [
        f"{json_path} contains duplicate {field} {value!r} at indexes {indexes}"
        for value, indexes in positions.items()
        if len(indexes) > 1
    ]
