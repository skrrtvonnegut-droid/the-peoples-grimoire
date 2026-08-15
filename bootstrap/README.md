# Bootstrap Kit

This directory contains the portable installation substrate for a private Grimoire instance.

The kit is intentionally split into four layers:

1. **Conversational protocol** — [`../BOOTSTRAP.md`](../BOOTSTRAP.md) tells a capable chatbot how to conduct discovery, planning, approval, application, verification, and handoff.
2. **Provider-neutral blueprints** — the invariant private-core and control-plane structures describe semantic roles without assuming a vendor.
3. **Carrier packs** — a carrier pack binds abstract roles to providers and declares what the chatbot host must be able to do.
4. **Validated artifacts** — bootstrap profiles and plans have public JSON Schemas and synthetic examples.

## Files

- [`blueprints/private-core.blueprint.json`](blueprints/private-core.blueprint.json) — invariant repository skeleton plus history-derived path rules.
- [`blueprints/control-plane.blueprint.json`](blueprints/control-plane.blueprint.json) — stable control-plane objects and relationships.
- [`carriers/notion-github.carrier.json`](carriers/notion-github.carrier.json) — first carrier binding: Notion for semantic memory and GitHub for versioned artifacts.
- [`../schemas/grimoire-bootstrap-profile.schema.json`](../schemas/grimoire-bootstrap-profile.schema.json) — approved discovery and topology contract.
- [`../schemas/grimoire-bootstrap-plan.schema.json`](../schemas/grimoire-bootstrap-plan.schema.json) — inspectable plan/apply contract.
- [`../examples/bootstrap/profile.synthetic.json`](../examples/bootstrap/profile.synthetic.json) — synthetic profile fixture.
- [`../examples/bootstrap/plan.synthetic.json`](../examples/bootstrap/plan.synthetic.json) — synthetic plan fixture.

## Invariant structure, adaptive domains

The installer always creates enough structure to remain governable:

- architecture;
- policies;
- manifests;
- registries;
- carrier bindings;
- workflows and automation;
- prompts and reusable artifacts;
- Garden Pass records; and
- archive and retirement guidance.

The installer does **not** decide domain folders in advance. `domains/{domain.slug}` paths come from the operator-approved profile, which is derived from repeated patterns in their authorized history.

This separation prevents two common failures:

- a universal second-brain template that does not resemble the operator’s life; and
- a literal export tree that reproduces every provider silo inside the new system.

## Adding another carrier pack

A new carrier pack should:

1. bind one or more abstract roles to named providers;
2. declare required search, read, create, update, link, export, and delete capabilities;
3. identify the host-managed authorization path;
4. map the provider-neutral blueprints into provider-native objects;
5. state what cannot be represented without loss;
6. define manual and read-only degraded modes;
7. preserve stable identities and one-authority-per-concern semantics; and
8. include only synthetic examples.

A carrier pack never contains credentials, live workspace identifiers, private repository names, personal history, or production payloads.

## Compatibility posture

The chatbot is an interface to the protocol, not the protocol itself. A host may implement the flow through connected tools, an MCP surface, local scripts, or manual work orders. The portable artifacts are the profile, plan, blueprints, stable IDs, and verification receipts.
