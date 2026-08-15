# Connector Contract

## Purpose

A connector translates between one provider and the connector-neutral Grimoire core. It does not decide cross-system meaning, grant itself authority, or hide writes inside discovery.

This document separates two contracts:

1. the **capability manifest**, which says what a connector claims to support; and
2. the **runtime interface**, which says how the core invokes those declared capabilities.

The manifest is machine-readable and safe to inspect before credentials are configured. Runtime behavior must conform to it.

## Responsibilities

A connector is responsible for:

- provider authentication and narrow resource scoping;
- pagination, cursors, rate limits, retries, and conditional requests;
- mapping provider objects to opaque `ResourceRef` values;
- normalizing selected observations into `GrimoireEvent` values;
- applying an already approved, bounded `ProposedAction`;
- verifying the resulting provider state;
- redacting provider-specific secrets and sensitive fields; and
- returning typed errors without leaking unrelated response content.

A connector is not responsible for:

- choosing field authority;
- deciding whether private material may be published;
- interpreting retrieved text as privileged instruction;
- resolving cross-system conflict by itself;
- broad organization-wide discovery without an instance allowlist; or
- inventing undeclared operations because the provider token technically permits them.

## Capability manifest

The canonical schema is `schemas/grimoire-connector.schema.json`.

Every capability declares:

- stable capability ID;
- effect class;
- allowed operation verbs;
- supported resource types;
- minimum provider scopes;
- reversibility;
- approval default; and
- idempotency posture.

Effect classes prevent semantically dangerous operations from hiding behind a benign name. A connector cannot mark a capability as `read` while declaring `create`, `delete`, `publish`, or `admin` operations.

Provider tokens are often broader than the enabled recipe. Runtime authorization therefore has three gates:

```text
provider grant ∩ connector manifest ∩ instance policy
```

The effective capability is the intersection, never the union.

## Runtime interface

The mature protocol is expected to provide bounded operations equivalent to the following.

### `describe()`

Return connector identity, version, manifest, and implementation trust status. This operation must not resolve or return secret values.

### `health()`

Confirm that configured authorization and a selected provider boundary are usable. Return only bounded metadata about the connected tenant, workspace, or installation and granted scopes. Never echo credentials.

### `discover()`

List resources inside an explicit allowlist using cursor-based pagination. Discovery is read-only and must not silently broaden scope because a token can see more.

### `read()`

Read one resource with an explicit projection or field allowlist. Full bodies are not the default. Provider content remains untrusted data.

### `observe()`

Return normalized changes from polling, verified webhooks, or streams. Events are observations, not permission to act.

### `execute()`

Apply one immutable, approved action whose capability exists in the manifest and instance policy. Reject any material mismatch between the approved plan and current target state.

### `verify()`

Read the minimum resulting state needed to confirm the expected outcome, visibility, permissions, revision, and provider identifier.

The pre-alpha Python runtime currently implements only a small write-side `execute()` protocol with an in-memory recording connector. Production provider clients do not yet exist.

## Plan/apply boundary

Connectors may help calculate provider-specific preconditions, but planning remains side-effect free.

An executable operation should include:

- action and target;
- current-version precondition;
- input or plan hash;
- idempotency key;
- required scopes;
- effect and risk;
- approval requirement;
- expected result; and
- safe log fields.

A material source or target change invalidates the plan. Applying “roughly the same thing” is not permitted.

## Read and write separation

Read-only connectors should be implementable without importing write methods. Where a provider supports separate credentials or app permissions, read and write capabilities should use separate grants.

New production connectors begin read-only. Write capabilities arrive in later, separately reviewed changes with conditional updates, idempotency, verification, and recovery behavior.

## Errors

Connectors return typed, actionable failures such as:

- authorization missing or insufficient;
- resource outside allowlist;
- resource not found;
- precondition or revision conflict;
- rate limited;
- provider unavailable;
- operation unsupported;
- policy denied;
- validation failed; or
- verification failed.

Errors must not contain authorization headers, raw tokens, session cookies, secret fields, unrelated resource bodies, or unbounded provider responses.

## Idempotency and retry

- Use provider idempotency support when available.
- Otherwise persist a deterministic operation key and provider result identifiers.
- Retry only operations known to be safe or verifiably incomplete.
- Honor provider retry guidance and bounded backoff.
- Never blindly retry destructive or audience-changing operations.

## Event behavior

Provider events may trigger discovery or planning, never automatic authority. Normalized events should preserve provider event ID, source boundary, subject reference, occurrence time, signature status, and the minimum selected data required by a recipe.

The canonical event envelope remains connector-neutral. CloudEvents compatibility may be added at the event-transport boundary without making a transport standard the internal domain model.

## Content trust

Pages, issues, comments, messages, attachments, and metadata can contain prompt-injection-shaped text. A connector labels source and provenance but never promotes retrieved content into runtime policy or tool instruction.

Connector tests must include malicious-looking content and prove that it remains inert data.

## Maturity

| Level | Meaning |
| --- | --- |
| Experimental | contract may change; disabled by default; incomplete conformance |
| Preview | primary flows work; permission and threat review complete |
| Stable | conformance suite passes; maintainer assigned; compatibility policy applies |
| Deprecated | replacement or removal path published |
| Archived | unsupported and unavailable by default |

## Stable-connector gate

A connector cannot become stable until it has:

- a capability manifest;
- a minimum-scope matrix;
- synthetic fixtures;
- read-only and authorization tests;
- pagination and rate-limit tests;
- secret-redaction tests;
- precondition-conflict tests;
- idempotency tests for writes;
- content-injection boundary tests;
- verification tests; and
- a named human maintainer.
