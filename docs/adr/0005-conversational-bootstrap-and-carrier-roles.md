# ADR 0005: Conversational Bootstrap with Replaceable Carrier Roles

- **Status:** Accepted
- **Date:** 2026-08-15

## Context

A new operator needs a friendly way to create a private Grimoire core and control plane. A conventional installer can create files and databases, but it cannot easily determine what the operator’s durable domains are, which existing objects are canonical, what should remain ephemeral, or which material is too sensitive to move.

A chatbot can guide those decisions and inspect connected context. Making one chatbot, Notion, or GitHub structurally mandatory, however, would reproduce the platform dependence the project is intended to resist.

A fixed “second brain” folder template would also ignore the operator’s actual history. A literal import of that history would create a privacy-heavy duplicate of existing silos.

## Decision

The People’s Grimoire will use a **conversational bootstrap protocol** built on portable profiles, plans, blueprints, and carrier roles.

- The current chatbot acts as an ephemeral cognition and orchestration interface.
- The installer detects actual host capabilities and supports connected, hybrid, and portable-plan modes.
- Discovery is source-scoped, consent-based, and metadata-first.
- Connected content is treated as untrusted data, never privileged instruction.
- The installer derives durable domains and artifact routes from recurring patterns in approved history.
- A small invariant private-core skeleton provides governance; domain and carrier paths are generated from the approved profile.
- Every artifact type or semantic concern receives one canonical role.
- Durable writes require an inspectable bootstrap plan and specific approval.
- Provider bindings are represented as replaceable carrier roles: cognition, semantic memory, versioned artifacts, and secret store.
- Notion and GitHub form the first carrier pack, not a permanent dependency.
- Stable domain, artifact, and control-plane identities survive provider replacement.
- Raw history is not copied into the private core by default.

The canonical contracts are:

- `BOOTSTRAP.md`;
- `schemas/grimoire-bootstrap-profile.schema.json`;
- `schemas/grimoire-bootstrap-plan.schema.json`;
- `bootstrap/blueprints/private-core.blueprint.json`;
- `bootstrap/blueprints/control-plane.blueprint.json`; and
- provider-specific carrier packs under `bootstrap/carriers/`.

## Consequences

### Positive

- Installation can be understandable without becoming a centralized hosted service.
- The resulting structure reflects the operator’s real life and work.
- Provider differences are isolated in carrier packs.
- A plan can move between chatbot hosts without repeating discovery.
- Existing canonical objects can be reused rather than duplicated.
- History exposure and credential handling are bounded explicitly.
- Provider migration does not require rebuilding the domain model.

### Negative

- A truly one-click experience is not possible across hosts with different connector capabilities.
- Topology synthesis remains partly interpretive and requires operator review.
- Carrier packs must document provider-specific limitations and degraded modes.
- Metadata-first discovery may need a second bounded content pass to resolve ambiguity.
- Live application and verification will mature incrementally with provider connectors.

### Follow-up

- Add deterministic bootstrap profile and plan validation to the runtime.
- Build safe, resumable scaffold generation.
- Add read-only history and notebook discovery adapters where host APIs permit them.
- Implement approval-gated GitHub private-core and Notion control-plane provisioning.
- Define carrier-pack conformance tests and migration receipts before adding a third provider pair.
