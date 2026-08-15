"""Shared loading, schema, and credential-scan helpers for trust manifests."""

from __future__ import annotations

import json
import re
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from importlib import resources
from pathlib import Path
from typing import Any

import yaml

SCHEMA_BY_KIND = {
    "grimoire.artifact": "grimoire-artifact.schema.json",
    "grimoire.connector": "grimoire-connector.schema.json",
    "grimoire.instance": "grimoire-instance.schema.json",
}

ALLOWED_SECRET_REFERENCE_PREFIXES = (
    "env:",
    "keyring:",
    "vault:",
    "secret-manager:",
    "op:",
)

SENSITIVE_KEY = re.compile(
    r"(^|_)(?:token|password|secret|api_key|client_secret|private_key|access_token|"
    r"refresh_token|credential|credentials|authorization|session_cookie)$",
    re.IGNORECASE,
)

TOKEN_VALUE = re.compile(
    r"^(?:gh[pousr]_|github_pat_|ntn_|sk-[A-Za-z0-9]|xox[baprs]-|"
    r"AKIA[0-9A-Z]{12,}|eyJ[A-Za-z0-9_-]{8,}|(?:Basic|Bearer)\s+[A-Za-z0-9._~+/=-]+)",
    re.IGNORECASE,
)

PRIVATE_KEY_VALUE = re.compile(r"-----BEGIN (?:[A-Z0-9 ]+ )?PRIVATE KEY-----")


class ValidationFailure(ValueError):
    """Raised when a document cannot be loaded or interpreted safely."""


@dataclass(frozen=True)
class ValidationResult:
    """Validation outcome for one file or directory boundary."""

    path: Path
    errors: tuple[str, ...]

    @property
    def ok(self) -> bool:
        return not self.errors


def _load_document(path: Path) -> Mapping[str, Any]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ValidationFailure(f"cannot read file: {exc}") from exc

    try:
        if path.suffix.lower() == ".json":
            data = json.loads(text)
        else:
            data = yaml.safe_load(text)
    except (json.JSONDecodeError, yaml.YAMLError) as exc:
        raise ValidationFailure(f"cannot parse document: {exc}") from exc

    if not isinstance(data, Mapping):
        raise ValidationFailure("top-level document must be an object/mapping")
    return data


def _load_schema(filename: str) -> Mapping[str, Any]:
    schema_path = resources.files("peoples_grimoire").joinpath("schemas", filename)
    return json.loads(schema_path.read_text(encoding="utf-8"))


def _format_json_path(parts: Iterable[object]) -> str:
    path = "$"
    for part in parts:
        if isinstance(part, int):
            path += f"[{part}]"
        else:
            path += f".{part}"
    return path


def _looks_like_reference(value: str) -> bool:
    return value.startswith(ALLOWED_SECRET_REFERENCE_PREFIXES)


def _scan_for_inline_secrets(node: Any, path: tuple[object, ...] = ()) -> list[str]:
    findings: list[str] = []

    if isinstance(node, Mapping):
        for raw_key, value in node.items():
            key = str(raw_key)
            normalized = key.lower().replace("-", "_")
            current_path = (*path, key)

            if isinstance(value, str):
                if SENSITIVE_KEY.search(normalized) and not normalized.endswith("_ref"):
                    if value and not _looks_like_reference(value):
                        findings.append(
                            f"{_format_json_path(current_path)} appears to contain an inline "
                            "credential; store a secret reference instead"
                        )
                elif TOKEN_VALUE.match(value.strip()) or PRIVATE_KEY_VALUE.search(value):
                    findings.append(
                        f"{_format_json_path(current_path)} resembles credential material; "
                        "store a secret reference instead"
                    )

            findings.extend(_scan_for_inline_secrets(value, current_path))

    elif isinstance(node, list):
        for index, value in enumerate(node):
            findings.extend(_scan_for_inline_secrets(value, (*path, index)))

    return findings
