# Connector Capability Manifest

A connector must declare its authority **before** an operator grants credentials or enables a recipe.

The manifest is both documentation and an executable refusal boundary. A connector implementation that happens to support an API call is not permitted to use it unless the exact Grimoire action, resource type, and required permission are declared.

## Files

- JSON Schema: [`schemas/connector-manifest.schema.json`](../../schemas/connector-manifest.schema.json)
- Synthetic GitHub example: [`examples/manifests/github.synthetic.json`](../../examples/manifests/github.synthetic.json)
- Synthetic Notion example: [`examples/manifests/notion.synthetic.json`](../../examples/manifests/notion.synthetic.json)
- Python model: `peoples_grimoire.connectors.ConnectorManifest`
- Conformance helpers: `peoples_grimoire.connectors.conformance`

The provider examples are synthetic protocol fixtures, not promises about a particular account, plan, or provider configuration.

## Manifest anatomy

| Section | Purpose |
| --- | --- |
| `schema_version` | Version of the manifest document shape |
| `name` and `version` | Connector identity and implementation release |
| `protocol_versions` | Exact Grimoire connector protocols the implementation accepts |
| `resource_types` | Provider-neutral resources the connector exposes |
| `capabilities` | Exact action names, operation class, resources, permissions, and safety properties |
| `authentication` | Supported credential mechanisms and baseline permissions |
| `delivery` | Polling and webhook support |
| `rate_limit` | Provider strategy and retry behavior |
| `sensitivity` | Sensitive fields, data classes, and default redaction |
| `deletion` | Provider deletion semantics and recovery support |
| `conformance` | Synthetic fixtures and test classes implemented by the connector |

Unknown document fields and unknown operation classes are rejected by the schema.

## Exact actions, not broad verbs

Each capability declares an exact `action`, such as `update_properties`, alongside one operation class:

- `read`
- `observe`
- `create`
- `update`
- `delete`

The operation class communicates impact. The action name is the actual allowlist key.

A manifest that declares `update_properties` does **not** implicitly permit `archive_page`, `delete_page`, or an arbitrary provider request. The runtime refuses an undeclared action before approval and before connector execution.

## Permission comparison

A recipe step declares:

- connector;
- exact action;
- resource type; and
- permissions it expects.

Evaluation occurs in two stages:

1. The recipe permissions must be contained within the manifest's baseline and capability-specific declaration.
2. The active credential must contain every permission required by the manifest.

An extra credential permission does not widen the manifest. An extra recipe permission causes refusal rather than opportunistic use.

The most restrictive layer wins:

```text
provider capability
∩ manifest declaration
∩ active credential
∩ recipe requirement
∩ local policy
∩ explicit approval
```

## Approval, idempotency, and reversibility

Every capability declares:

- whether repeating it is idempotent;
- whether it supports conditional updates;
- whether its effect may be irreversible; and
- whether explicit approval is required.

A recipe cannot weaken a connector's approval requirement. If either the recipe action or capability requires approval, the exact action ID must be approved.

Irreversible operations remain visible in the capability decision so interfaces can require elevated review. Read and observe capabilities cannot be declared irreversible.

## Protocol compatibility

Manifest schema version and connector protocol version are separate.

- `schema_version` describes the JSON document.
- `protocol_versions` explicitly lists the runtime protocols accepted by the connector.
- The current reference runtime protocol is `0.1`.
- Compatibility is explicit, not inferred. A connector must list `0.1` to run under `0.1`.
- A future protocol is not assumed compatible merely because it shares a major or minor number.
- Additive manifest fields require a new schema version; behavior changes require a protocol decision and migration notes.

This exact-match rule is conservative while the project is pre-alpha. A broader compatibility policy can be adopted only through an architecture decision and conformance coverage.

## Conformance harness

`check_manifest_conformance` verifies protocol support, synthetic fixtures, declared tests, and sensitive-field coverage.

`check_connector_conformance` verifies that an implementation's identity, manifest, granted-permission representation, and execution interface agree.

`check_connector_behavior` accepts synthetic cases and verifies that:

- declared actions are allowed when scopes are present;
- undeclared actions are denied;
- optional synthetic execution returns `ExecutionResult`; and
- test transports fail without leaking exception messages.

Production connector packages should run the reusable harness against a fake or recording transport. Conformance tests must never require live personal accounts.

## Validation

```bash
python -m pip install -e ".[dev]"
pytest tests/test_connector_capabilities.py
```

The test suite validates the JSON Schema, loads both synthetic manifests into the Python contract, checks fixture paths, compares recipe permissions, refuses undeclared writes, and exercises the recording connector.
