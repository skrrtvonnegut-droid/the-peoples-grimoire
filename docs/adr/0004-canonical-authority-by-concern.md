# ADR 0004: Canonical Authority by Concern

- **Status:** Accepted
- **Date:** 2026-08-15

## Context

ADR 0003 assigns field-level authority so that Notion and GitHub are not treated as blindly synchronized copies. The project also needs stable identities for durable artifacts and a clear answer to where a promoted representation becomes authoritative.

A simplistic “one canonical application per artifact” rule would erase the legitimate division of labor between systems. The opposite rule—allowing every linked representation to be co-equal—would make conflicts and provenance ambiguous.

## Decision

The People’s Grimoire will assign one canonical authority **per semantic concern**.

- A logical artifact may have multiple external representations.
- Each meaningful concern names exactly one authoritative representation or the local registry.
- Other representations are references, derived views, or explicitly managed mirrors.
- A promotion may change authority for a named concern only through a reviewable rule.
- Ambiguous or conflicting authority fails closed with `hold-and-surface` behavior.
- Last-write-wins is not the default for meaningful content.

Artifact manifests record stable identity, representations, classification, and concern authority. Recipes remain responsible for movement and transformation. Connectors remain responsible for provider translation and bounded execution.

## Consequences

### Positive

- Stable artifact identity complements rather than replaces field authority.
- Notion and GitHub can remain native homes for different concerns.
- Promotion from draft knowledge to versioned artifact becomes explicit.
- Drift and conflict can be explained in human terms.
- The registry can remain metadata-minimal.

### Negative

- Artifact registration requires a small authority map.
- New concerns may require migration or review.
- Cross-document validation cannot prove semantic correctness by itself.
- Explicit mirrors require ongoing reconciliation policy.

## Alternatives considered

### One canonical application per artifact

Rejected because a project narrative, issue state, accepted ADR, and cross-system identity naturally belong to different systems.

### Last-write-wins synchronization

Rejected because timestamps do not express meaning, authorship, or authority and can silently destroy intentional edits.

### No canonical authority

Rejected because every conflict would become an ad hoc judgment and automated behavior would be impossible to explain reliably.

## Security and privacy implications

Authority does not grant movement permission. Classification, target visibility, connector capability, instance policy, and approval remain separate gates. A canonical private representation may not be published merely because it is authoritative.
