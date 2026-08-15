# ADR 0003: Field-Level Authority Instead of Blind Bidirectional Sync

- **Status:** Accepted
- **Date:** 2026-08-15

## Context

Connected applications often contain overlapping but semantically different representations. A GitHub issue and a Notion task may both have a title and status, but their workflows and meanings are not necessarily identical.

A generic two-way synchronization engine tends to create loops, overwrite intentional edits, or rely on last-write-wins.

## Decision

Every recipe must define authority at the field or semantic-concern level.

- A whole application is not automatically the source of truth.
- Recipes declare read direction, write direction, transformation, conflict behavior, and approval requirements per field.
- The default conflict strategy is hold-and-surface.
- Last-write-wins is permitted only for explicitly low-risk fields and must be documented.
- Derived fields, including AI summaries, cannot overwrite authoritative source fields.

## Consequences

### Positive

- Synchronization behavior is legible.
- Conflict handling reflects meaning rather than timestamp accidents.
- Applications retain their native strengths.
- Loops and silent overwrites are easier to prevent.

### Negative

- Recipes require more design work.
- Mappings may vary by community and use case.
- Some fields will remain intentionally unsynchronized.

### Follow-up

Define a machine-readable authority section in the recipe schema and build conflict fixtures for the Notion–GitHub MVP.
