# Roadmap

The roadmap is capability-based rather than date-driven. Each phase must preserve the privacy and approval boundaries established before it.

## Phase 0 — Foundation

**Goal:** make the project legible before it becomes powerful.

- [x] Public vision and principles.
- [x] Federated architecture decision.
- [x] Privacy and trust boundary.
- [x] Human-accountable AI maintenance decision.
- [x] Canonical event JSON Schema.
- [x] Python reference models.
- [x] Dry-run and approval-gated execution scaffold.
- [x] Sanitized configuration and recipe examples.
- [ ] Durable issue backlog and connector research notes.
- [ ] License, dependency, and supply-chain review.

## v0.1 — Readable memory

**Goal:** observe Notion and GitHub safely and connect identities without production writes.

- Durable SQLite state and migrations.
- Connector capability manifest schema.
- GitHub read connector for repositories, issues, pull requests, and releases.
- Notion read connector for explicitly configured pages and databases.
- Polling cursors and replay protection.
- Link graph and project-link CLI.
- Recipe parser and validation.
- Redacted structured logging.
- Export and deletion commands.
- End-to-end synthetic fixtures.

**Release gate:** a user can link a project, observe changes, inspect normalized events, and export or delete local state without granting write access.

## v0.2 — Guarded action

**Goal:** introduce writes without introducing invisible authority.

- Serializable action plans.
- Persistent approval queue.
- Conditional updates and idempotency controls.
- Notion property update action.
- GitHub branch and draft pull request action.
- Notion decision → ADR proposal recipe.
- GitHub issue → Notion task-view recipe.
- Verification and compensation metadata.
- Conflict records and hold-and-surface workflow.

**Release gate:** no production write occurs without an inspectable plan, explicit authority rule, approval evidence, and audit record.

## v0.3 — Connector kit

**Goal:** make a third connector possible without changing the core.

- Versioned connector protocol.
- Capability manifest tooling.
- Contract and conformance tests.
- Synthetic fixture generator.
- Permission and data-class documentation template.
- Connector development CLI.
- Reference connector package structure.
- Compatibility policy.

**Release gate:** an independent contributor can build and test a read-only connector from public documentation.

## v0.4 — Composable recipes

**Goal:** let communities share coordination patterns safely.

- Versioned recipe schema.
- Recipe linting and simulation.
- Parameter and secret injection.
- Policy bundles.
- Provenance and AI-processing declarations.
- Recipe signing or integrity metadata.
- Public recipe catalog format.
- Migration behavior across recipe versions.

## v0.5 — Multiple interfaces

**Goal:** ensure no single interface owns the system.

- Local HTTP API.
- CLI approval and inspection.
- Optional web dashboard.
- Assistant-facing tool contract.
- Webhook ingress with signature verification.
- Event subscriptions and filtered views.

## Later horizons

- Additional connectors selected through community demand and maintainer capacity.
- Team roles and multi-operator approval.
- Encrypted local content cache.
- Distributed or replicated local-first state.
- Standards interoperability.
- Federated recipe and connector discovery.
- Independent runtime implementations.

## Cross-cutting requirements

Every phase includes:

- privacy review;
- threat-model updates;
- least-privilege documentation;
- synthetic fixtures;
- replay and idempotency tests;
- export and deletion behavior;
- accessibility and plain-language documentation; and
- migration notes for stored state.

## Explicitly deferred

The project will not prioritize the following before the trust model is proven:

- a hosted multi-tenant SaaS product;
- broad organization-wide indexing;
- automatic destructive actions;
- opaque autonomous agents;
- full-content replication;
- marketplace monetization; or
- dozens of shallow connectors.

The first job is not to connect everything. It is to establish a way of connecting things that deserves trust.
