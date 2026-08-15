# Canonical Homes and Authority by Concern

A connected system becomes unreliable when two representations quietly believe they are equally authoritative. The Grimoire avoids this with a scoped rule:

> Every durable concern has one canonical authority. Other representations reference, derive, summarize, or explicitly mirror it.

## Why “by concern” matters

A whole project rarely belongs to one application.

For a Notion and GitHub project:

| Concern | Canonical authority |
| --- | --- |
| Long-form project narrative | Notion project page |
| Repository identity and default branch | GitHub repository |
| Issue state and pull-request merge state | GitHub |
| Accepted decision text | Merged ADR in Git |
| Draft decision exploration | Notion, until promoted |
| Cross-system identity | Local Grimoire registry |
| AI-generated summary | Derived representation; never source truth |

This preserves the project’s existing field-authority model while adding stable artifact identity. “One truth” does not mean forcing one platform to own every field. It means that a particular semantic concern cannot have two silent masters.

## Representation roles

- **Canonical:** authoritative for at least one declared concern.
- **Reference:** points to the artifact without reproducing its body.
- **Derived:** generated from canonical material and replaceable.
- **Mirror:** an intentionally managed copy with explicit drift and conflict rules.

Mirrors are exceptional. They require a declared reason, scope, verification rule, and conflict policy.

## Promotion

Moving an artifact from living knowledge into versioned publication is a promotion, not an invisible synchronization event.

A safe promotion:

1. identifies source concern and canonical representation;
2. classifies the material and target visibility;
3. inventories attachments, metadata, links, and hidden fields;
4. transforms and sanitizes deliberately;
5. renders an inspectable diff;
6. creates a branch and pull request rather than writing the default branch;
7. records provenance and the resulting representation; and
8. changes authority only when the promotion rule says it should.

For example, a decision may be drafted in Notion. Once the ADR pull request merges, the accepted decision text becomes canonical in Git while Notion retains a link and evolving implementation context.

## Drift

Drift is not automatically an error. A reference may intentionally contain less information, and a derived summary may lag briefly.

Drift becomes a conflict when two representations change the same declared concern in incompatible ways. The default response is **hold and surface**:

- stop mutation;
- show both fingerprints or diffs;
- name the authority rule;
- explain the last successful reconciliation; and
- request a human decision when policy cannot resolve it safely.

Last-write-wins is not an acceptable default for meaningful knowledge.

## Stable identity

Titles and locations change. Durable artifacts therefore receive stable IDs such as:

```text
artifact.knowledge.connector-contract
artifact.decision.canonical-authority
artifact.project.example-lantern
```

External locators remain provider-specific references. The local registry stores only the metadata needed to find and relate them; it does not need to become another full-content silo.
