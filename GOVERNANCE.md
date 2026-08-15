# Governance

## Purpose

The People’s Grimoire is a public technical commons. Governance should keep it useful, safe, plural, and resistant to capture by any single vendor, interface, investor, or automated system.

## Founding stance

The project’s normative direction is stated in the [Manifesto](MANIFESTO.md): build technology that returns time, agency, knowledge, and infrastructure to the people who create and depend upon it.

The [founding vow](MANIFESTO.md#founding-vow) names compassion as a governance obligation. It does not require religious assent. It requires the project to examine who gains agency, who absorbs risk, whether consent and exit are real, and whether a technically successful change leaves people constrained by existing material conditions safer and more sovereign.

This stance is not decorative branding and it is not a substitute for technical evidence. It informs how evidence is interpreted and which trade-offs the project is willing to make. In practice, governance should:

- distribute authority rather than quietly centralize it;
- prefer interoperable commons over proprietary enclosure;
- evaluate automation by whose drudgery it reduces, whose power it increases, and who bears its risks;
- prioritize the agency and safety of people most constrained by existing material conditions;
- treat dignity, accessibility, care, repair, and belonging as legitimate system outcomes;
- refuse efficiencies that depend on surveillance, coerced participation, hidden labor, or human disposability;
- reject behavioral surveillance, coercive automation, and extraction as default business models;
- preserve plural participation, including queer and non-normative ways of living and organizing;
- value maintenance, documentation, accessibility, teaching, and care as infrastructure; and
- keep exit, export, deletion, refusal, and self-hosting meaningful.

A proposal that materially conflicts with the Manifesto or founding vow must state that conflict plainly and justify why the divergence serves the people affected. Convenience, growth, efficiency, or vendor access alone is not sufficient justification.

## Maintainer model

The project uses an **AI-assisted lead-maintainer workflow with a human maintainer of record**.

### Human maintainer of record

The repository owner is accountable for:

- repository access and credentials;
- merges, releases, and package publication;
- licensing and legal decisions;
- security and privacy response;
- community moderation;
- appointment or removal of maintainers; and
- final intervention when consensus fails.

### AI-assisted architecture and maintenance

AI systems may:

- draft architecture and documentation;
- implement scoped changes;
- propose issues and roadmaps;
- review code and identify risk;
- summarize discussions;
- maintain traceability between decisions and implementation; and
- help coordinate work across connected systems.

AI systems do not independently:

- hold project credentials;
- accept legal responsibility;
- merge security-sensitive changes without human review;
- make binding community conduct decisions;
- publish releases; or
- authorize production access to contributor data.

This boundary is described in [ADR 0002](docs/adr/0002-ai-assisted-human-accountability.md).

## Contributor roles

### Contributor

Anyone who reports an issue, improves documentation, proposes a recipe, writes code, reviews a change, or helps another participant.

### Connector maintainer

A contributor trusted to review and maintain one connector or connector family.

### Core maintainer

A contributor trusted to review core runtime, schema, security, and release changes.

### Maintainer of record

The human account holder responsible for final repository and community accountability.

Roles are earned through sustained, constructive work and may be scoped to particular areas.

## Decision process

### Routine changes

Ordinary fixes and documentation changes are decided through pull request review.

### Architectural changes

Changes affecting protocol contracts, state models, trust boundaries, connector semantics, or long-term compatibility require an Architecture Decision Record.

An ADR should state:

- context;
- decision;
- alternatives considered;
- consequences;
- migration impact; and
- security or privacy implications.

### Security, privacy, licensing, and governance

These changes require explicit human maintainer review even when technically generated or reviewed by AI.

### Consensus and disagreement

The default approach is rough consensus supported by written rationale and working evidence.

When consensus is not available:

1. identify the reversible experiment;
2. prefer the choice that preserves user sovereignty, shared power, and future optionality;
3. record dissent and trade-offs;
4. time-box the experiment through a release boundary; and
5. let the maintainer of record decide only when a decision is necessary.

## Pull request requirements

A mergeable change should include, where applicable:

- a clear problem statement;
- tests or fixtures;
- documentation;
- privacy and permission impact;
- user-agency and anti-capture impact;
- compassion impact: who becomes safer or more sovereign, who could be harmed or made disposable, and how that risk is mitigated;
- migration behavior;
- provenance for generated or transformed material;
- disclosure of material AI assistance; and
- confirmation that examples contain no personal data.

## Release governance

Releases require:

- passing automated checks;
- a reviewed change summary;
- migration notes;
- dependency and secret scanning;
- known-risk disclosure;
- signed or otherwise attributable publication by the human maintainer of record; and
- a rollback or recovery path appropriate to the release.

Pre-alpha versions make no compatibility guarantee. Compatibility policy will be established before v0.1.

## Independence

The project may integrate with commercial applications but should not grant any vendor privileged governance rights in exchange for access, sponsorship, investment, or distribution.

Sponsorships and material conflicts of interest must be disclosed. Funding arrangements must not override the Manifesto, privacy model, or community governance without an explicit public amendment.

## Amendments

Governance changes use a pull request and written rationale. Substantive amendments require the human maintainer of record to approve them.
