import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, ValidationError, validate

from peoples_grimoire.connectors import (
    CapabilityRequirement,
    ConnectorBehaviorCase,
    ConnectorManifest,
    RecordingConnector,
    assert_connector_conforms,
    check_connector_behavior,
)
from peoples_grimoire.models import ProposedAction, ResourceRef

ROOT = Path(__file__).parents[1]
SCHEMA = json.loads((ROOT / "schemas/connector-manifest.schema.json").read_text())


@pytest.mark.parametrize(
    "path",
    [
        ROOT / "examples/manifests/github.synthetic.json",
        ROOT / "examples/manifests/notion.synthetic.json",
    ],
)
def test_synthetic_manifests_match_schema_and_runtime_model(path: Path) -> None:
    value = json.loads(path.read_text())

    Draft202012Validator.check_schema(SCHEMA)
    validate(value, SCHEMA)
    manifest = ConnectorManifest.from_mapping(value)

    assert manifest.to_dict() == value
    assert all((ROOT / fixture).exists() for fixture in manifest.fixtures)


def test_schema_rejects_unknown_operation() -> None:
    value = json.loads(
        (ROOT / "examples/manifests/github.synthetic.json").read_text()
    )
    value["capabilities"][0]["operation"] = "patch"

    with pytest.raises(ValidationError):
        validate(value, SCHEMA)


def test_recipe_permissions_cannot_exceed_manifest_declaration() -> None:
    value = json.loads(
        (ROOT / "examples/manifests/github.synthetic.json").read_text()
    )
    manifest = ConnectorManifest.from_mapping(value)
    requirement = CapabilityRequirement(
        connector="github",
        action="read_issue",
        resource_type="issue",
        permissions=frozenset({"administration:write"}),
    )

    decision = manifest.evaluate_requirement(
        requirement,
        granted_permissions={"metadata:read", "issues:read", "administration:write"},
    )

    assert not decision.allowed
    assert decision.code == "undeclared_recipe_permissions"
    assert decision.undeclared_permissions == frozenset({"administration:write"})


def test_action_requires_declared_and_granted_permissions() -> None:
    value = json.loads(
        (ROOT / "examples/manifests/notion.synthetic.json").read_text()
    )
    manifest = ConnectorManifest.from_mapping(value)
    action = ProposedAction(
        target=ResourceRef("notion", "page", "synthetic-page"),
        action="update_properties",
        changes={"status": "done"},
        reason="Synthetic conformance check.",
    )

    missing = manifest.evaluate_action(action, granted_permissions={"content:read"})
    allowed = manifest.evaluate_action(action, granted_permissions={"content:write"})

    assert missing.code == "missing_permissions"
    assert missing.missing_permissions == frozenset({"content:write"})
    assert allowed.allowed
    assert allowed.requires_approval


def test_recording_connector_passes_reusable_conformance_harness() -> None:
    connector = RecordingConnector(name="notion")

    assert_connector_conforms(connector)


def test_behavior_harness_exercises_declared_and_denied_actions() -> None:
    connector = RecordingConnector(name="notion")
    declared = ProposedAction(
        target=ResourceRef("notion", "page", "synthetic-page"),
        action="update_properties",
        changes={"status": "done"},
        reason="Synthetic declared behavior.",
    )
    denied = ProposedAction(
        target=ResourceRef("notion", "page", "synthetic-page"),
        action="undeclared_write",
        changes={},
        reason="Synthetic denied behavior.",
    )

    report = check_connector_behavior(
        connector,
        [
            ConnectorBehaviorCase(
                action=declared,
                expect_allowed=True,
                execute=True,
            ),
            ConnectorBehaviorCase(
                action=denied,
                expect_allowed=False,
            ),
        ],
    )

    report.require()
    assert connector.actions == [declared]
