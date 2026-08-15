# Privacy and Trust

## Objective

The People’s Grimoire exists to return coherence and agency to the operator. It must not become another surveillance layer, credential honeypot, or central owner of a person’s digital life.

Privacy is therefore an architectural constraint, not a feature to add later.

## Trust boundaries

| Boundary | May contain | Must not contain |
|---|---|---|
| Public repository | Protocols, source code, schemas, synthetic examples, redacted fixtures | Personal content, credentials, private identifiers, production payloads |
| Private deployment configuration | Connector aliases, recipe choices, opaque resource mappings | Plaintext secrets, unnecessary document bodies, broad exports |
| Secret manager or protected environment | Access tokens, refresh tokens, signing secrets | Source code, logs, shared examples |
| Local state store | Opaque references, event fingerprints, approvals, redacted audit records | Unbounded raw content unless explicitly enabled and encrypted |
| Diagnostic output | Correlation IDs, connector names, status, redacted errors | Tokens, authorization headers, private text, full webhook payloads |

A private Git repository is **not** a secret manager.

## Data classes

### Public

Documentation, schemas, synthetic fixtures, connector capability descriptions, and data explicitly intended for publication.

### Operational metadata

Opaque identifiers, timestamps, recipe names, action states, rate-limit data, and correlation identifiers. This can still reveal patterns and should be protected.

### Private content

Document titles, issue bodies, comments, messages, names, email addresses, workspace structure, and relationship mappings.

### Secrets

Tokens, cookies, client secrets, private keys, signing secrets, and recovery material.

### High-impact data

Authentication records, health information, financial information, legal records, employment records, precise location, intimate communications, and other data whose exposure or manipulation could materially harm a person.

High-impact connectors and recipes require explicit threat modeling and stronger approval rules before release.

## Threat model

The initial threat model includes:

1. **Credential disclosure** through Git, logs, exceptions, fixtures, or support requests.
2. **Over-permissioned connectors** that can read or write more than a recipe requires.
3. **Prompt or content injection** embedded in connected documents and interpreted as instructions.
4. **Confused deputy behavior** where one connector causes an action outside the operator’s intended scope.
5. **Silent data corruption** from blind bidirectional synchronization.
6. **Replay and duplication** of webhook events or planned actions.
7. **Cross-instance leakage** in a team or hosted deployment.
8. **Inference from metadata** even when document bodies are not stored.
9. **Supply-chain compromise** in connector dependencies or community recipes.
10. **AI overreach** when generated interpretations are treated as authoritative facts or commands.

## Required controls

### Data minimization

Connectors request and retain only fields needed by an enabled recipe.

### Least privilege

Each connector documents its minimum permissions. Read and write credentials should be separated when the external platform permits it.

### Dry-run by default

New connectors and recipes begin in read-only or plan-only mode. Writes require an explicit configuration change and may still require per-action approval.

### Provenance

Every normalized event and proposed action records where it came from. AI-generated summaries or classifications are labeled as derived, not source truth.

### Content is data, not instruction

Text retrieved from a SaaS application must never automatically become privileged runtime instructions. Connectors and planners treat external content as untrusted input.

### Redaction

Logging utilities must redact authorization headers, tokens, cookies, secret-shaped values, and configured sensitive fields before output is persisted.

### Retention

Operational records define a retention policy. Deletion and export are supported without requiring continued access to the original SaaS application.

### Reversibility

Recipes identify whether an operation can be reversed, compensated, or only manually repaired. Irreversible or destructive operations require elevated approval.

### Isolation

Connector credentials, state, and queues are isolated by instance. Team deployments should further isolate users or projects where appropriate.

## Public contribution rules

Bug reports and pull requests must use synthetic or aggressively redacted examples.

Do not submit:

- screenshots of private workspaces;
- copied webhook bodies;
- live repository or page identifiers;
- real names, email addresses, issue content, or internal URLs;
- tokens that have merely been truncated; or
- logs before reviewing them for sensitive data.

A reproducible fixture should preserve the **shape of the bug**, not the identity of the person who experienced it.

## AI-assisted processing

AI may help classify, summarize, link, or propose actions. It must not silently change the authority model.

Recipes using AI must declare:

- what data is sent to the model;
- whether processing is local or remote;
- what retention terms apply;
- what output is considered advisory;
- what confidence or uncertainty is recorded; and
- what actions still require human approval.

Model output is evidence for a plan, not permission to execute it.

## Minimum deployment checklist

Before connecting a production account:

- [ ] The connector permissions have been reviewed.
- [ ] Secrets are stored outside Git.
- [ ] Dry-run is enabled.
- [ ] Logs have been tested for redaction.
- [ ] The recipe defines field authority and conflict behavior.
- [ ] Replay and duplicate events have been tested.
- [ ] Destructive actions are disabled or separately approved.
- [ ] A state backup and recovery method exists.
- [ ] The operator understands what data leaves the local boundary.
- [ ] Synthetic fixtures reproduce expected behavior.

## Reporting a privacy or security problem

Follow [SECURITY.md](../SECURITY.md). Do not publish sensitive details in a public issue.
