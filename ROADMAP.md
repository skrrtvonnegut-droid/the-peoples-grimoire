# Roadmap

The roadmap translates the [Manifesto](MANIFESTO.md) into capability. It is capability-based rather than date-driven. Each phase must preserve the privacy, approval, user-agency, and anti-capture boundaries established before it.

## Phase 0 — Foundation

**Goal:** make the project legible before it becomes powerful.

- [x] Founding manifesto and public stance.
- [x] Public vision and principles.
- [x] Federated architecture decision.
- [x] Privacy and trust boundary.
- [x] Human-accountable AI maintenance decision.
- [x] Canonical event JSON Schema.
- [x] Python reference models.
- [x] Dry-run and approval-gated execution scaffold.
- [x] Sanitized configuration and recipe examples.
- [x] Connector capability manifest and protocol contract.
- [x] Deny-by-default structured observability.
- [x] Conversational bootstrap protocol.
- [x] Provider-neutral private-core and control-plane blueprints.
- [x] Notion and GitHub starter carrier pack.
- [x] Bootstrap profile and plan schemas with synthetic validation fixtures.
- [ ] Durable issue backlog and connector research notes.
- [ ] License, dependency, and supply-chain review.

## Bootstrap track — Guided genesis

**Goal:** let a new operator create a private core and semantic control plane through a chatbot without surrendering the result to that chatbot or accepting a generic second-brain template.

- [x] Single-file chatbot entrypoint and human installation guide.
- [x] Readiness, consent, discovery, topology, plan, approval, apply, verification, and handoff state model.
- [x] Metadata-first, source-scoped history discovery rules.
- [x] Invariant private-core skeleton with history-derived domain paths.
- [x] Provider-neutral control-plane object model.
- [x] Portable carrier roles and Notion/GitHub binding.
- [x] Connected, hybrid, and portable-plan degraded modes.
- [ ] Runtime validation for bootstrap profiles and plans.
- [ ] Deterministic scaffold generator with dry-run and apply separation.
- [ ] Resumable checkpoints and plan invalidation on target drift.
- [ ] Chat-history and notebook discovery adapters where host APIs permit them.
- [ ] Approval-gated private GitHub core provisioning.
- [ ] Approval-gated Notion control-plane reconciliation and provisioning.
- [ ] Export, migration, disconnect, and complete deletion receipts.
- [ ] Carrier-pack conformance tests and an alternate-provider fixture.

**Release gate:** a new operator can bring the public kit to a compatible chatbot, approve a bounded discovery scope, review a history-shaped topology, create or reuse a private core and control plane through specific approvals, verify the result, and move the portable profile and plan to another host without repeating discovery.

## v0.1 — Readable memory

**Goal:** observe Notion and GitHub safely and connect identities without production writes.

- [ ] Durable SQLite state and migrations.
- [x] Connector capability manifest schema.
- [ ] GitHub read connector for repositories, issues, pull requests, and releases.
- [ ] Notion read connector for explicitly configured pages and databases.
- [ ] Polling cursors and replay protection.
- [ ] Link graph and project-link CLI.
- [ ] Recipe parser and validation.
- [x] Redacted structured logging.
- [ ] Export and deletion commands.
- [ ] End-to-end synthetic fixtures.

**Release gate:** a user can link a project, observe changes, inspect normalized events, and export or delete local state without granting write access.

## v0.2 — Guarded action

**Goal:** introduce writes without introducing invisible authority.

- [ ] Serializable action plans.
- [ ] Persistent approval queue.
- [x] Conditional-update and idempotency declarations.
- [ ] Notion property update action.
- [ ] GitHub branch and draft pull request action.
- [ ] Notion decision → ADR proposal recipe.
- [ ] GitHub issue → Notion task-view recipe.
- [ ] Verification and compensation metadata.
- [ ] Conflict records and hold-and-surface workflow.

**Release gate:** no production write occurs without an inspectable plan, explicit authority rule, approval evidence, and audit record.

## v0.3 — Connector and carrier kit

**Goal:** make a third connector or replacement carrier possible without changing the core or the operator’s domain model.

- [x] Versioned connector protocol.
- [x] Capability manifest tooling.
- [x] Contract and conformance tests.
- [ ] Synthetic fixture generator.
- [ ] Permission and data-class documentation template.
- [ ] Connector development CLI.
- [ ] Reference connector package structure.
- [ ] Carrier-pack schema and conformance harness.
- [ ] Stable-identity migration receipt between two semantic-memory carriers.
- [x] Compatibility policy.

**Release gate:** an independent contributor can build and test a read-only connector or carrier binding from public documentation, and an operator can replace one carrier without reconstructing their domain topology.

## v0.4 — Composable recipes

**Goal:** let communities share coordination patterns safely.

- [ ] Versioned recipe schema.
- [ ] Recipe linting and simulation.
- [ ] Parameter and secret injection.
- [ ] Policy bundles.
- [ ] Provenance and AI-processing declarations.
- [ ] Recipe signing or integrity metadata.
- [ ] Public recipe catalog format.
- [ ] Migration behavior across recipe versions.

## v0.5 — Multiple interfaces

**Goal:** ensure no single interface owns the system.

- [ ] Local HTTP API.
- [ ] CLI approval and inspection.
- [ ] Optional web dashboard.
- [ ] Assistant-facing tool contract.
- [ ] Webhook ingress with signature verification.
- [ ] Event subscriptions and filtered views.

## Later horizons

- Additional connectors selected through community demand and maintainer capacity.
- Swappable semantic-memory carriers such as local notebooks, knowledge graphs, or federated stores.
- Swappable versioned-artifact carriers such as GitLab, Forgejo, or local Git.
- Community-governed connector, carrier-pack, and recipe commons.
- Cooperative hosting patterns that do not create a new platform landlord.
- Labor-saving automation evaluated by time returned, not activity extracted.
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
- user-agency and anti-capture review;
- bootstrap portability and host-capability detection;
- synthetic fixtures;
- replay and idempotency tests;
- export and deletion behavior;
- accessibility and plain-language documentation; and
- migration notes for stored state.

## Explicitly deferred

The project will not prioritize the following before the trust model is proven:

- a hosted multi-tenant SaaS product;
- broad organization-wide indexing;
- unbounded chat-history or notebook ingestion;
- automatic destructive actions;
- opaque autonomous agents;
- full-content replication;
- marketplace monetization;
- behavioral advertising or surveillance infrastructure;
- automation designed primarily to intensify labor or evade accountability; or
- dozens of shallow connectors.

The first job is not to connect everything. It is to establish a way of connecting things that deserves trust—and returns power to the people using it.
