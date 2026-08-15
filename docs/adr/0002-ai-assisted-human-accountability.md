# ADR 0002: AI-Assisted, Human-Accountable Maintenance and Operation

- **Status:** Accepted
- **Date:** 2026-08-15

## Context

AI systems can help design architecture, write code, interpret connected information, triage issues, and propose actions. The project itself is partly motivated by using an intelligent interface across fragmented SaaS systems.

An AI system, however, cannot be the legal owner of a repository, protect credentials independently, accept community responsibility, or bear the consequences of a harmful merge or production action.

## Decision

The project will use an **AI-assisted lead-maintainer workflow with human accountability**.

For project maintenance:

- AI may draft issues, documentation, code, reviews, and release notes.
- AI-generated changes follow the same review, test, security, and privacy requirements as human-generated changes.
- The human maintainer of record remains accountable for credentials, merges, releases, moderation, licensing, and security response.
- Security-sensitive, destructive, or governance changes require identifiable human review.
- AI assistance should be disclosed when it materially shaped a contribution.

For runtime operation:

- AI output is treated as derived evidence, not an authoritative command.
- Consequential actions require explicit policy and, by default, human approval.
- Untrusted content retrieved from connected applications is never promoted into privileged instructions.
- Provenance records when a model contributed to a classification, summary, link, or plan.

## Consequences

### Positive

- The project can benefit from rapid AI-assisted development without pretending accountability disappeared.
- Contributors can inspect and challenge machine-generated reasoning through ordinary artifacts.
- Runtime actions remain bounded by policy and consent.

### Negative

- Some automation will remain slower because a person must review it.
- AI-generated contributions may require additional verification.
- Governance must distinguish assistance from authority.

### Follow-up

Create contribution disclosure guidance and tests for content-as-data boundaries.
