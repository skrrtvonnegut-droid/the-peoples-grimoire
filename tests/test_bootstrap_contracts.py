from __future__ import annotations

import copy
import json
from pathlib import Path, PurePosixPath

import pytest
from jsonschema import Draft202012Validator, FormatChecker, ValidationError

ROOT = Path(__file__).resolve().parents[1]


def load_json(relative_path: str) -> dict:
    return json.loads((ROOT / relative_path).read_text(encoding="utf-8"))


def validator_for(relative_path: str) -> Draft202012Validator:
    schema = load_json(relative_path)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def test_synthetic_bootstrap_profile_validates() -> None:
    validator = validator_for("schemas/grimoire-bootstrap-profile.schema.json")
    profile = load_json("examples/bootstrap/profile.synthetic.json")

    validator.validate(profile)


def test_synthetic_bootstrap_plan_validates() -> None:
    validator = validator_for("schemas/grimoire-bootstrap-plan.schema.json")
    plan = load_json("examples/bootstrap/plan.synthetic.json")

    validator.validate(plan)


def test_personal_profile_cannot_allow_employer_confidential_material() -> None:
    validator = validator_for("schemas/grimoire-bootstrap-profile.schema.json")
    profile = load_json("examples/bootstrap/profile.synthetic.json")
    invalid = copy.deepcopy(profile)
    invalid["instance"]["classification_boundary"]["allowed"].append(
        "employer_confidential"
    )

    with pytest.raises(ValidationError):
        validator.validate(invalid)


def test_ephemeral_artifact_route_cannot_claim_a_durable_canonical_home() -> None:
    validator = validator_for("schemas/grimoire-bootstrap-profile.schema.json")
    profile = load_json("examples/bootstrap/profile.synthetic.json")
    invalid = copy.deepcopy(profile)
    route = invalid["domains"][1]["artifact_routes"][0]
    route["canonical_role"] = "semantic_memory"

    with pytest.raises(ValidationError):
        validator.validate(invalid)


def test_write_actions_always_require_specific_approval() -> None:
    validator = validator_for("schemas/grimoire-bootstrap-plan.schema.json")
    plan = load_json("examples/bootstrap/plan.synthetic.json")
    invalid = copy.deepcopy(plan)
    invalid["actions"][0]["requires_approval"] = False

    with pytest.raises(ValidationError):
        validator.validate(invalid)


def test_private_core_blueprint_paths_are_relative_and_provider_neutral() -> None:
    blueprint = load_json("bootstrap/blueprints/private-core.blueprint.json")
    providers = {"notion", "github", "chatgpt", "claude", "gemini"}

    for item in blueprint["invariants"]:
        path = PurePosixPath(item["path"])
        assert not path.is_absolute()
        assert ".." not in path.parts
        assert not providers.intersection(part.lower() for part in path.parts)

    assert blueprint["generated_paths"][0]["path_pattern"] == "domains/{domain.slug}/"
    assert (
        blueprint["generated_paths"][1]["path_pattern"]
        == "carriers/{carrier.role}/{carrier.provider}/"
    )


def test_carrier_pack_blueprint_references_resolve() -> None:
    pack_path = ROOT / "bootstrap/carriers/notion-github.carrier.json"
    pack = json.loads(pack_path.read_text(encoding="utf-8"))

    for role in ("semantic_memory", "versioned_artifacts"):
        relative_reference = pack["roles"][role]["blueprint"]
        resolved = (pack_path.parent / relative_reference).resolve()
        assert resolved.is_file()
        assert ROOT.resolve() in resolved.parents


def test_profile_role_names_match_their_carrier_slots() -> None:
    profile = load_json("examples/bootstrap/profile.synthetic.json")

    for slot, binding in profile["carriers"].items():
        assert binding["role"] == slot
