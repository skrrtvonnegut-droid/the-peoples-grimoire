# ADR 0006: Continuity Must Outlive the AI Interface

- **Status:** Accepted
- **Date:** 2026-08-28

## Context

The People’s Grimoire uses a chatbot as its cognition and orchestration interface, while durable knowledge, versioned artifacts, identity, provenance, and policy live in external user-controlled carriers. Existing architecture already treats the chatbot as an ephemeral carrier rather than a canonical owner, but that implication needs to be elevated into an explicit design requirement.

Conversation history, model memory, and vendor-specific personalization can make an assistant more useful, but they are not reliable foundations for continuity. They may be incomplete, inaccessible to another host, difficult to export, or structurally tied to a single vendor. If a Grimoire can only continue its work because one chatbot remembers prior conversations, then the person does not yet own the continuity of the system.

The project therefore needs a concrete standard for AI portability that goes beyond abstract provider neutrality.

## Decision

The People’s Grimoire adopts **continuity over interface** as a core design philosophy.

The chatbot or AI host is a **replaceable cognition carrier**, not the canonical owner of a Grimoire instance.

A mature Grimoire must preserve enough durable context outside any single conversation, model, or vendor that a capable replacement AI can enter the system with no prior chat history, inspect the operator-authorized durable layers, and continue the operator’s work intelligently and traceably.

This becomes the **fresh-host continuity test**.

A conforming instance should allow a fresh capable AI, using only the public bootstrap protocol and the operator-authorized durable carriers, to determine at least:

- what the Grimoire instance is and whom it serves;
- which durable domains exist and how they relate;
- which system is authoritative for each relevant artifact type or semantic concern;
- how stable identities and cross-system links are represented;
- what policies, permissions, classifications, and approval boundaries apply;
- which projects or workflows are currently active;
- where the canonical artifacts for that work live;
- what important decisions, provenance, and unresolved conflicts must be preserved; and
- how to continue work without silently inventing missing state.

The test does **not** require a replacement model to reproduce hidden chain-of-thought, undocumented conversational mannerisms, or identical model behavior. It requires recoverable system state, provenance, operating conventions, and enough explicit context for safe continuation.

The following rules follow from this decision:

1. Chat history and model memory may be discovery inputs, but they are not canonical runtime dependencies.
2. Stable identity, routing, source-of-truth rules, provenance, project state, and durable procedures must live in operator-authorized external carriers when they are needed for future continuation.
3. Provider-specific prompts, instructions, or integrations should be separated from provider-neutral semantics wherever practical.
4. Replacing the cognition provider must not require rebuilding the operator’s domain model or manually recreating durable knowledge from old conversations.
5. Architectural changes that create undocumented dependence on one model’s private memory should be treated as portability regressions unless deliberately bounded and surfaced.
6. Bootstrap, handoff, migration, and conformance procedures should include a fresh-host continuity check.

## Consequences

### Positive

- The operator retains continuity even when changing chatbot vendors or models.
- The Grimoire becomes a durable personal knowledge system rather than an elaborate chat archive.
- Canonical state becomes easier to inspect, audit, migrate, and reconcile.
- AI hosts can improve independently without becoming the owner of the operator’s intellectual history.
- Bootstrap quality gains a concrete acceptance test instead of relying on subjective confidence.
- The system encourages explicit provenance, current-state records, and maintainable handoff artifacts.

### Negative

- Some context that feels effortless inside a long-running conversation must be distilled into durable form when it matters.
- Operators and maintainers must decide what state is important enough to preserve rather than treating all chat history as memory.
- A fresh host may still interpret the same durable context differently; portability of state does not imply identical cognition.
- Maintaining current project state, manifests, and handoff records adds modest operational overhead.

## Follow-up

- Add continuity over interface to the public README principles.
- Add the fresh-host continuity test to the bootstrap verification protocol.
- Document cognition-provider replacement alongside other carrier swaps.
- Add future conformance fixtures that test whether a synthetic fresh host can recover topology, authority, and active-work state from durable artifacts alone.
- Prefer future schemas and control-plane records that expose resumable state without requiring raw conversation archives.
