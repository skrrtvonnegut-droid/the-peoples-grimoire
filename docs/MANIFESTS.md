# Trust Manifests

Trust manifests make authority, permissions, classification, and deployment boundaries inspectable before a connector receives access to a real account.

They are configuration and contract documents, not containers for copied SaaS content.

## Manifest kinds

### `grimoire.connector`

A connector capability manifest declares what one adapter can do:

- provider and connector version;
- supported resource types;
- authentication methods;
- capability effects and operations;
- minimum provider scopes;
- reversibility and approval defaults;
- event mechanisms and signature behavior;
- data-retention and logging defaults; and
- conformance status.

A capability has one effect class:

| Effect | Typical operations | Default posture |
| --- | --- | --- |
| `read` | discover, search, read, observe | policy-controlled or automatic after bounded authorization |
| `write` | create, update | explicit policy or approval |
| `destructive` | delete, archive | required approval or forbidden |
| `audience-changing` | publish, invite, message | required approval or forbidden |
| `administrative` | deploy, purchase, admin | required approval or forbidden |

The schema rejects an operation whose effect is misdeclared—for example, `create` hidden inside a read capability.

### `grimoire.instance`

An instance manifest is private deployment configuration. It selects connector manifests, enables named capabilities, bounds each connector with a resource allowlist, and declares approval policy.

It may contain a secret reference such as:

```yaml
credential_ref: env:GRIMOIRE_GITHUB_TOKEN
```

It must never contain the token value itself.

The example v0.1 instance forbids writes, deletion, and publication. This reflects the current release goal: readable memory before production action.

### `grimoire.artifact`

An artifact manifest gives one durable logical object a stable identity across systems. It records small amounts of registry metadata, not the artifact body.

An artifact may have several external representations, but authority is assigned once per semantic concern. A Notion page may be authoritative for project narrative while a GitHub repository is authoritative for repository identity and issue state.

This is the operational meaning of **one truth, many references**: one authority for each concern, not one application forced to own every concern.

## Classification vocabulary

| Sensitivity | Meaning |
| --- | --- |
| `public` | intentionally safe for broad disclosure |
| `operational` | low-content metadata that still reveals system activity or structure |
| `private` | non-public personal, team, or workspace material |
| `confidential` | organization-, customer-, tenant-, or relationship-specific material |
| `high-impact` | data whose exposure or manipulation could materially harm a person |
| `secret` | credential or recovery material; content is reference-only |
| `unknown` | not yet classified; fails closed at publication boundaries |

Publication status is separate from sensitivity. Material is not public merely because names were removed, and a public source does not grant republication rights to copied content.

## Bundle validation

Run:

```bash
grimoire validate examples/manifests
```

Validation performs:

1. JSON Schema Draft 2020-12 validation;
2. likely inline-secret detection;
3. duplicate capability, resource, representation, and authority checks;
4. artifact-authority reference checks;
5. instance-to-connector capability resolution; and
6. policy checks that reject enabled write, destructive, publication, or administrative effects when the instance forbids them.

A single-file validation checks the file in isolation. Directory validation treats all typed manifests below that directory as one bundle and resolves cross-document references.

## Canonical schema location

The public specifications live under `schemas/`. Byte-identical copies under `src/peoples_grimoire/schemas/` are packaging mirrors included in the Python distribution. CI verifies that they do not drift.

Schema versioning is independent from package versioning. Breaking schema changes require migration notes and, when they alter core semantics or trust boundaries, an Architecture Decision Record.

## Synthetic examples only

The example bundle uses fictional identifiers. A contributor must not create a “realistic” fixture by lightly anonymizing a personal workspace, employer tenant, private repository, webhook payload, or production log. Preserve the shape of the behavior, not the identity of the person or organization that produced it.
