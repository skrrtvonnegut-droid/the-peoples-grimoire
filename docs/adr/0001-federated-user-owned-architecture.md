# ADR 0001: Federated, User-Owned Architecture

- **Status:** Accepted
- **Date:** 2026-08-15

## Context

The project seeks to create a coherent system across many SaaS applications. The easiest technical path would be to copy all connected data into a central service and make that service the primary interface.

That design would reproduce the dependency and ownership problem the project is intended to solve. It would also create a high-value store of private content and credentials.

## Decision

The People’s Grimoire will use a federated, local-first architecture.

- External applications retain their native data.
- The core stores minimal references, links, event fingerprints, policies, and audit records.
- Raw content is fetched only when a recipe requires it.
- A mandatory hosted control plane is prohibited.
- Connectors and recipes use open, versioned contracts.
- Operators control deployment, credentials, retention, export, and deletion.

Optional hosted deployments may exist later, but they must implement the same portable contracts and cannot become required for protocol participation.

## Consequences

### Positive

- Operators retain meaningful control.
- The central privacy blast radius is smaller.
- Connectors can evolve independently.
- Alternative runtimes and interfaces can interoperate.
- Public recipes can be shared without publishing private content.

### Negative

- Setup is more complex than a fully managed central service.
- Some cross-system queries require live access to source applications.
- Identity resolution and conflict handling must be explicit.
- Team deployments need careful state and credential isolation.

### Follow-up

Define export formats, connector capability manifests, and a durable local state model before v0.1.
