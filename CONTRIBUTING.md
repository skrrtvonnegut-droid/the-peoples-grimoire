# Contributing

Thank you for helping build connective tissue rather than another silo.

The project is pre-alpha. Small, inspectable contributions are more useful than broad rewrites.

## Before opening a pull request

For a new connector, recipe, schema change, or architectural change, open an issue first. Explain:

- the user problem;
- the smallest useful capability;
- the external permissions required;
- the data classes involved;
- the proposed source-of-truth rules;
- failure and conflict behavior; and
- how the change can be tested with synthetic data.

Small documentation corrections and focused bug fixes may go directly to a pull request.

## Development setup

Requirements:

- Python 3.11 or newer;
- Git; and
- no production SaaS credentials.

```bash
git clone https://github.com/skrrtvonnegut-droid/the-peoples-grimoire.git
cd the-peoples-grimoire

python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"

ruff check .
pytest
grimoire validate examples/manifests
```

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

## Branches and commits

Use a focused branch such as:

```text
feature/github-event-normalizer
fix/approval-replay
docs/connector-threat-model
```

Prefer small commits with messages that describe the outcome.

## Pull request checklist

- [ ] The change has one coherent purpose.
- [ ] Tests cover the intended behavior and important failure paths.
- [ ] New fixtures are synthetic and contain no private identifiers.
- [ ] Permission changes are documented.
- [ ] Logging does not expose content or secrets.
- [ ] Writes remain behind plan/apply and approval boundaries.
- [ ] Replay and idempotency behavior has been considered.
- [ ] Documentation and schemas are updated.
- [ ] Material AI assistance is disclosed.
- [ ] The contributor has reviewed the full diff.

## AI-assisted contributions

AI-assisted contributions are welcome.

The human contributor remains responsible for:

- understanding the submitted change;
- verifying generated code and citations;
- checking licenses and provenance;
- removing private or fabricated data;
- running tests;
- explaining trade-offs; and
- responding to review.

In the pull request, briefly state how AI materially contributed, for example:

> AI assistance: drafted the initial connector contract and tests; I reviewed and revised all behavior and verified the official API documentation.

Do not paste private connected content into an external model merely to create a fixture or bug report.

## Connector requirements

A connector contribution should include:

1. capability manifest validated against `schemas/grimoire-connector.schema.json`;
2. authentication and minimum-permission documentation;
3. supported resource and action matrix;
4. rate-limit and retry behavior;
5. webhook or polling semantics;
6. idempotency and precondition behavior;
7. redaction rules;
8. deletion behavior;
9. synthetic fixtures; and
10. conformance tests.

A connector must not perform a write during discovery, normalization, or planning. Its runtime operations may not exceed the intersection of provider authorization, declared connector capabilities, and instance policy.

## Recipe requirements

A recipe must declare:

- trigger and scope;
- identity resolution;
- field authority;
- transformations;
- conflict strategy;
- approval requirements;
- proposed actions;
- verification;
- reversibility;
- redaction;
- AI-processing behavior, when present; and
- recipe version.

## Architecture decisions

Use the ADR format in `docs/adr/` for durable technical choices.

Do not rewrite an accepted ADR to hide history. Add a new ADR that supersedes it.

## Privacy

Read [Privacy and Trust](docs/PRIVACY.md) and [Trust Manifests](docs/MANIFESTS.md) before submitting logs, examples, or connector fixtures.

A useful bug report preserves the shape of the failure, not the identity of the person who experienced it.

## Conduct

Participation is governed by [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
