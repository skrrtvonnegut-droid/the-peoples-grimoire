# ADR 0005: Compassion is an engineering requirement

- **Status:** Accepted
- **Date:** 2026-08-15

## Context

The Manifesto names liberation as the project’s horizon, and the founding vow names active compassion as its ethical center. Without a durable technical interpretation, compassion could remain ceremonial language while ordinary engineering incentives continue to optimize throughput, adoption, or institutional convenience at someone else’s expense.

Compassion cannot be reduced to a metric, and it cannot mean paternalistically deciding what is best for other people. The project still needs a repeatable way to ask whether a technically successful change reduces suffering, expands agency, and avoids transferring hidden costs onto people with less power.

## Decision

Compassion is a cross-cutting engineering and governance requirement for The People’s Grimoire.

For consequential changes, design and review must:

1. Identify the people and communities materially affected, especially those most constrained by the existing system.
2. State who gains time, authority, access, safety, or saved labor—and who absorbs risk, maintenance, displacement, surveillance, or dependency.
3. Treat consent, accessibility, dignity, repair, meaningful exit, reversibility, and refusal as system qualities rather than optional polish.
4. Prefer designs that expand a person’s practical choices without requiring broader data collection, centralized control, or coerced participation.
5. Refuse to call an automation liberatory merely because it is efficient. Labor saved by making people more disposable, precarious, surveilled, or afraid is not a successful outcome.
6. Preserve human authority over consequential actions and make uncertainty, conflict, and provenance inspectable.
7. Seek evidence and affected-user input as the project develops; no maintainer, institution, or AI system may define another person’s good solely on their behalf.

The founding vow is a spiritual and ethical orientation, not a religious test. Contributors do not need to share any particular cosmology or practice. Participation requires respect for the material obligation it names: compassion must move from intention into concrete safeguards, shared power, and useful aid.

This decision is implemented through the Manifesto, Governance, contribution requirements, architecture review, connector contracts, recipe design, and future acceptance criteria.

## Alternatives considered

### Keep the vow only in the Manifesto

Rejected. A vow that does not alter engineering decisions becomes branding.

### Remove spiritual language and retain only secular principles

Rejected. This would make the project more conventionally neutral by erasing part of its actual founding meaning. The project can remain plural without pretending it was born without commitments.

### Require contributors to affirm a shared spiritual framework

Rejected. Doctrinal conformity would contradict the project’s plural, commons-oriented architecture and turn an invitation to compassion into a gatekeeping mechanism.

## Consequences

- Proposals require more explicit power and harm analysis.
- Some apparently efficient integrations will be rejected or redesigned.
- Review may move more slowly when affected people, consent boundaries, or hidden labor are unclear.
- Maintainers must guard against both extractive optimization and paternalistic overreach.
- Compassion-related claims remain open to evidence, correction, dissent, and changing community knowledge.
- The project gains a durable test: technical power is justified only when it is bounded by care and increases the real sovereignty of the people it touches.

This constraint intentionally slows the exercise of power so that freedom, safety, and trust can grow first.
