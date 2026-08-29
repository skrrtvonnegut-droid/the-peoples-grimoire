# Install Your Grimoire

The primary installer for **The People’s Grimoire** is a guided conversation.

For the default GitHub + Notion carrier pack, installation should feel like this:

> **Connect GitHub. Connect Notion. Paste one prompt. Review the plan.**

You do not need to clone this repository or manually assemble the bootstrap kit when your chatbot can read the public People’s Grimoire repository through GitHub or ordinary public web access. The repository remains the canonical installer source; the prompt simply tells the chatbot where to find it and how to begin safely.

> [!WARNING]
> The bootstrap kit is **pre-alpha**. It defines a safe, portable installation protocol and synthetic contracts. Support for live reads and writes depends on the capabilities exposed by the chatbot host and its connected integrations.

## What you need

- A capable chatbot that can read the public GitHub repository.
- A GitHub account for the default private, versioned core.
- A Notion workspace for the default semantic control plane.
- GitHub and Notion connected through the chatbot host’s official integrations or connectors.
- A willingness to review the proposed topology and bootstrap plan before durable writes occur.

GitHub and Notion are the first carrier pair, not permanent dependencies. The bootstrap profile names abstract roles so future carrier packs can substitute GitLab, Forgejo, Obsidian, Anytype, a local Git repository, or another compatible system.

## 1. Connect GitHub and Notion to your chatbot

Use the chatbot host’s official connection or integration flow. Start with the narrowest available access that can support the installation you want.

- Do **not** paste access tokens, cookies, client secrets, private keys, recovery codes, or comparable credentials into the conversation.
- Do **not** place credentials in either the public repository or the private core.
- The installer begins read-only and requests approval before durable write phases.
- A connection is not consent to inspect everything in that account. The bootstrap protocol still requires a bounded discovery scope.

If a host cannot connect one of the carriers directly, the installer should switch to hybrid or portable-plan mode rather than pretending it has access.

## 2. Paste the installer prompt

Start a new conversation with the chatbot you want to use as the cognition and orchestration interface for your Grimoire. Then paste the prompt below.

```text
I want to install my own instance of The People’s Grimoire.

Use your connected GitHub capabilities to locate the public repository:
https://github.com/skrrtvonnegut-droid/the-peoples-grimoire

Treat that repository, not this prompt, as the canonical installer source. Read BOOTSTRAP.md and the supporting bootstrap files, carrier definitions, schemas, blueprints, and documentation that BOOTSTRAP.md requires. Use the latest version available from the repository’s default branch unless I explicitly choose another version.

First verify your actual capabilities and my GitHub and Notion connections. Never ask me to paste credentials or secrets into chat. If a required connector is unavailable, say so and use the repository’s documented hybrid or portable-plan mode instead of pretending you have access.

Then execute BOOTSTRAP.md beginning at Phase 0.

Start read-only. Search before creating anything. Ask me to approve a bounded discovery scope before inspecting private history or content. Use approved history as evidence for my topology, not as cargo to indiscriminately copy into the Grimoire. Reuse existing canonical GitHub and Notion structures where appropriate.

Produce the readiness report, topology proposal, validated bootstrap profile, and bootstrap plan required by the protocol. Do not create, update, move, or delete durable objects until you have shown me the concrete plan and I explicitly approve that plan and its targets.

After approval, apply only the approved changes, keep the private instance private and secret-free, reconcile the GitHub private core with the Notion semantic control plane, verify the result, run the fresh-host continuity test, and give me the final apply receipt and operator handoff.

Do not write my private instance data back into the public People’s Grimoire repository.
```

A standalone copy of this prompt lives in [`INSTALL_PROMPT.md`](INSTALL_PROMPT.md).

The prompt is intentionally short enough to remain understandable and portable. It does not duplicate the full installer logic. Instead, it hands control to the canonical [`BOOTSTRAP.md`](BOOTSTRAP.md), which can evolve without requiring people to discover and copy a newer giant prompt.

## 3. Let the chatbot run the guided installation

A conforming assistant should lead you through eight stages:

1. **Readiness** — verify the current chatbot, public repository access, connected carriers, and missing capabilities.
2. **Consent and scope** — choose which history, notebooks, repositories, pages, databases, and classifications may be inspected.
3. **Read-only discovery** — inventory selected sources metadata-first and search for existing canonical objects.
4. **Topology** — infer durable domains, artifact types, workflows, lifecycle states, and canonical homes from recurring patterns.
5. **Plan** — produce a validated bootstrap profile and an inspectable list of proposed writes.
6. **Approval** — obtain specific approval for the GitHub and Notion changes.
7. **Build** — create or update the private core and semantic control plane without duplicating existing canonical objects.
8. **Verify and hand off** — test routing and fresh-host continuity, record a Garden Pass, and explain how to administer, export, migrate, or retire the instance.

The assistant should explain decisions in ordinary language and ask only for choices it cannot safely infer.

## What the default installation creates

### Private core in GitHub

A private, secret-free repository containing:

- architecture and source-of-truth rules;
- data classification, consent, retention, and routing policies;
- carrier bindings;
- a system manifest and domain topology;
- bridge and artifact registries;
- reusable workflows, prompts, and automation;
- history-derived domain folders; and
- Garden Pass records for durable maintenance history.

The invariant skeleton is defined in [`bootstrap/blueprints/private-core.blueprint.json`](bootstrap/blueprints/private-core.blueprint.json). Domain folders are generated from the approved bootstrap profile rather than copied from a universal template.

### Semantic control plane in Notion

A root control surface that reuses existing pages and databases where possible and establishes stable identities for:

- the System Manifest;
- the Bridge Registry;
- Garden Pass history;
- the Domain Index; and
- an optional Artifact Registry when the operator has reusable prompts, code, skills, or other versioned objects.

The provider-neutral object model is defined in [`bootstrap/blueprints/control-plane.blueprint.json`](bootstrap/blueprints/control-plane.blueprint.json).

## How personalization works

The installer looks for recurring patterns rather than isolated topics. It considers:

- repeated conversation themes and project names;
- the kinds of artifacts you repeatedly create;
- active workflows and maintenance rhythms;
- whether material is living knowledge, versioned configuration, a temporary conversation, or an archive;
- sensitivity and data classification;
- existing Notion and GitHub structures that should be reused; and
- where each semantic concern already has a trustworthy canonical home.

The result should usually be a small number of durable domains with several artifact routes—not hundreds of folders named after individual chats.

## Privacy defaults

- History access is source-by-source and scope-limited.
- Metadata and summaries are preferred over full conversation bodies.
- Raw history is not committed to the private core by default.
- Personal Private material may enter a private instance.
- Professional Portfolio material may be sanitized for public GitHub only through an intentional publication step.
- Employer Confidential material stays in an employer-approved system or remains ephemeral.
- Secrets never belong in the Grimoire registry, repository, prompt, issue, log, or chat transcript.
- Text found in connected sources is always treated as untrusted data, never as installer instructions.
- Private instance data must never be written back into the public People’s Grimoire repository.

## Why this is prompt-first instead of clone-first

The public repository is the **installer authority**. The prompt is only the **invocation surface**.

That separation matters because a copied installation prompt can become stale. A small prompt that tells the chatbot to locate the repository and execute the current bootstrap protocol lets the public commons improve while preserving a stable onboarding ritual:

> **connect two services → paste one prompt → review → approve → verify**

It also reinforces the larger architectural principle that the chatbot is an interface to durable protocols and state, not their permanent owner.

## Fallback and manual mode

If the chatbot cannot read the public repository, provide it with [`BOOTSTRAP.md`](BOOTSTRAP.md) and the supporting `bootstrap/`, `schemas/`, and `examples/bootstrap/` directories.

A chatbot without direct GitHub or Notion write access can still complete discovery and planning. It should produce:

- a validated bootstrap profile;
- a bootstrap plan;
- a private-core file tree and file contents;
- a Notion build checklist; and
- verification and rollback instructions.

The operator can then apply those artifacts manually or move the plan to another compatible host without repeating discovery.

## Read next

- [`INSTALL_PROMPT.md`](INSTALL_PROMPT.md) — copy/paste bootstrap prompt.
- [`BOOTSTRAP.md`](BOOTSTRAP.md) — canonical executable conversational installer.
- [`docs/BOOTSTRAP_PROTOCOL.md`](docs/BOOTSTRAP_PROTOCOL.md) — architecture and state model.
- [`bootstrap/README.md`](bootstrap/README.md) — kit contents and extension points.
- [`docs/PRIVACY.md`](docs/PRIVACY.md) — privacy and trust boundaries.
