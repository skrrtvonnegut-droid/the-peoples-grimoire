from __future__ import annotations

import json
import shutil
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

from peoples_grimoire.validation import validate_document, validate_path


REPO_ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_ROOT = REPO_ROOT / "examples" / "manifests"
SCHEMA_ROOT = REPO_ROOT / "schemas"
PACKAGE_SCHEMA_ROOT = REPO_ROOT / "src" / "peoples_grimoire" / "schemas"


def test_example_bundle_validates() -> None:
    results = validate_path(EXAMPLE_ROOT)
    assert len(results) == 4
    assert all(result.ok for result in results), results


def test_inline_token_is_rejected(tmp_path: Path) -> None:
    manifest = tmp_path / "unsafe.yaml"
    manifest.write_text(
        """
kind: grimoire.instance
schema_version: "0.1.0"
instance:
  id: instance.unsafe
  name: Unsafe
  mode: local-first
policy:
  default_sensitivity: private
  unknown_sensitivity: deny
  secret_handling: references-only
  approvals:
    read: required
    write: forbidden
    delete: forbidden
    publish: forbidden
systems:
  github:
    connector_manifest: connector.github-readonly
    token: ghp_this_is_not_allowed
    enabled_capabilities: [capability.github.repository-read]
    resource_allowlist: [github://example/repository]
state:
  registry: sqlite:///state.db
  audit: sqlite:///state.db
""".strip(),
        encoding="utf-8",
    )

    result = validate_document(manifest)
    assert not result.ok
    assert any(
        "inline credential" in error or "credential material" in error
        for error in result.errors
    )


def test_secret_reference_is_allowed() -> None:
    result = validate_document(EXAMPLE_ROOT / "instance.yaml")
    assert result.ok, result.errors


def test_private_key_material_is_rejected(tmp_path: Path) -> None:
    manifest = tmp_path / "unsafe-key.yaml"
    manifest.write_text(
        """
kind: grimoire.instance
schema_version: "0.1.0"
instance:
  id: instance.unsafe-key
  name: Unsafe Key
  mode: local-first
policy:
  default_sensitivity: private
  unknown_sensitivity: deny
  secret_handling: references-only
  approvals:
    read: required
    write: forbidden
    delete: forbidden
    publish: forbidden
systems:
  github:
    connector_manifest: connector.github-readonly
    private_key: |-
      -----BEGIN PRIVATE KEY-----
      definitely-not-safe
      -----END PRIVATE KEY-----
    enabled_capabilities: [capability.github.repository-read]
    resource_allowlist: [github://example/repository]
state:
  registry: sqlite:///state.db
  audit: sqlite:///state.db
""".strip(),
        encoding="utf-8",
    )

    result = validate_document(manifest)
    assert not result.ok
    assert any("credential" in error for error in result.errors)


def test_malformed_typed_document_is_not_silently_skipped(tmp_path: Path) -> None:
    malformed = tmp_path / "broken.yaml"
    malformed.write_text(
        "kind: grimoire.instance\ninstance: [not: valid",
        encoding="utf-8",
    )

    results = validate_path(tmp_path)
    assert len(results) == 1
    assert not results[0].ok
    assert any("cannot parse document" in error for error in results[0].errors)


def test_unknown_enabled_capability_fails_bundle_validation(tmp_path: Path) -> None:
    bundle = tmp_path / "manifests"
    shutil.copytree(EXAMPLE_ROOT, bundle)
    instance_path = bundle / "instance.yaml"
    instance = yaml.safe_load(instance_path.read_text(encoding="utf-8"))
    instance["systems"]["github"]["enabled_capabilities"].append("capability.github.admin")
    instance_path.write_text(yaml.safe_dump(instance, sort_keys=False), encoding="utf-8")

    results = validate_path(bundle)
    instance_result = next(result for result in results if result.path.name == "instance.yaml")
    assert not instance_result.ok
    assert any("unknown capability" in error for error in instance_result.errors)


def test_forbidden_write_effect_fails_bundle_validation(tmp_path: Path) -> None:
    bundle = tmp_path / "manifests"
    shutil.copytree(EXAMPLE_ROOT, bundle)

    connector_path = bundle / "connectors" / "github.yaml"
    connector = yaml.safe_load(connector_path.read_text(encoding="utf-8"))
    connector["capabilities"].append(
        {
            "id": "capability.github.file-update",
            "effect": "write",
            "operations": ["update"],
            "resource_types": ["repository"],
            "required_scopes": ["contents:write"],
            "reversibility": "compensating",
            "approval_default": "required",
            "idempotency": "conditional",
        }
    )
    connector_path.write_text(yaml.safe_dump(connector, sort_keys=False), encoding="utf-8")

    instance_path = bundle / "instance.yaml"
    instance = yaml.safe_load(instance_path.read_text(encoding="utf-8"))
    instance["systems"]["github"]["enabled_capabilities"].append(
        "capability.github.file-update"
    )
    instance_path.write_text(yaml.safe_dump(instance, sort_keys=False), encoding="utf-8")

    results = validate_path(bundle)
    instance_result = next(result for result in results if result.path.name == "instance.yaml")
    assert not instance_result.ok
    assert any("approvals.write is forbidden" in error for error in instance_result.errors)


def test_artifact_authority_must_reference_declared_representation(tmp_path: Path) -> None:
    artifact_path = tmp_path / "artifact.yaml"
    artifact = yaml.safe_load((EXAMPLE_ROOT / "artifact.yaml").read_text(encoding="utf-8"))
    artifact["authority"][0]["representation"] = "representation.example.missing"
    artifact_path.write_text(yaml.safe_dump(artifact, sort_keys=False), encoding="utf-8")

    result = validate_document(artifact_path)
    assert not result.ok
    assert any("not declared in $.representations" in error for error in result.errors)


def test_connector_effect_rejects_mismatched_operation(tmp_path: Path) -> None:
    connector_path = tmp_path / "connector.yaml"
    connector = yaml.safe_load(
        (EXAMPLE_ROOT / "connectors" / "github.yaml").read_text(encoding="utf-8")
    )
    connector["capabilities"][0]["operations"] = ["create"]
    connector_path.write_text(yaml.safe_dump(connector, sort_keys=False), encoding="utf-8")

    result = validate_document(connector_path)
    assert not result.ok
    assert any("create" in error for error in result.errors)


def test_schema_mirrors_match_canonical_files() -> None:
    for canonical in sorted(SCHEMA_ROOT.glob("grimoire-*.schema.json")):
        package_copy = PACKAGE_SCHEMA_ROOT / canonical.name
        assert package_copy.read_bytes() == canonical.read_bytes(), canonical.name


def test_schemas_are_valid_draft_2020_12() -> None:
    for schema_path in sorted(SCHEMA_ROOT.glob("grimoire-*.schema.json")):
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
