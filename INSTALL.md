# Install Your Grimoire

The primary installer for The People’s Grimoire is a guided conversation.

You bring the public bootstrap kit into a chatbot you trust, connect the services you want to use through that chatbot’s own integration interface, and let the assistant help you design a private core around the life and work you already have. The installer does not impose a generic “second brain” taxonomy before it has inspected your actual patterns.

> [!WARNING]
> The bootstrap kit is **pre-alpha**. It defines a safe, portable installation protocol and synthetic contracts. Support for live reads and writes depends on the capabilities exposed by the chatbot host and its connected integrations.

## What you need

- A chatbot that can read uploaded files or a connected GitHub repository.
- A GitHub account for the default private, versioned core.
- A Notion workspace for the default semantic control plane.
- A willingness to review the proposed structure before anything is created.

GitHub and Notion are the first carrier pair, not permanent dependencies. The bootstrap profile names abstract roles so future carrier packs can substitute GitLab, Forgejo, Obsidian, Anytype, a local Git repository, or another compatible system.

## 1. Get the bootstrap kit

```bash
git clone https://github.com/skrrtvonnegut-droid/the-peoples-grimoire.git
cd the-peoples-grimoire
```

Downloading the repository as an archive also works.

## 2. Connect your carriers through the chatbot UI

Use the chatbot host’s official connection or integration flow to connect GitHub and Notion. Start with the narrowest available access.

- Do **not** paste access tokens, cookies, client secrets, private keys, or recovery codes into the conversation.
- Do **not** place credentials in either the public repository or the private core.
- The installer should begin read-only and request approval before every durable write phase.

When a host cannot connect one of the carriers directly, the installer must switch to a manual handoff rather than pretending it has access.

## 3. Give the kit to your chatbot

Use whichever method the host supports:

- share the repository through a connected GitHub integration;
- upload `BOOTSTRAP.md` together with the `bootstrap/`, `schemas/`, and `examples/bootstrap/` folders; or
- paste the contents of `BOOTSTRAP.md` into a new conversation.

Then send:

> Read `BOOTSTRAP.md` and execute the bootstrap protocol. Begin with readiness and capability detection. Do not create or modify anything until you have shown me the proposed topology and bootstrap plan.

## 4. Walk through the guided installation

The assistant should lead you through eight stages:

1. **Readiness** — identify the current chatbot, connected tools, and missing capabilities.
2. **Consent and scope** — choose which history, notebooks, repositories, and classifications may be inspected.
3. **Read-only discovery** — inventory selected sources metadata-first and search for existing canonical objects.
4. **Topology** — infer durable domains, artifact types, workflows, lifecycle states, and canonical homes from recurring patterns.
5. **Plan** — produce a validated bootstrap profile and an inspectable list of proposed writes.
6. **Approval** — obtain specific approval for the GitHub and Notion changes.
7. **Build** — create or update the private core and semantic control plane without duplicating existing canonical objects.
8. **Verify and hand off** — test routing, record a Garden Pass, and explain how to administer, export, migrate, or remove the instance.

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

The invariant skeleton is defined in [`bootstrap/blueprints/private-core.blueprint.json`](bootstrap/blueprints/private-core.blueprint.json). The domain folders are generated from your approved bootstrap profile rather than copied from a universal template.

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

## Manual mode

A chatbot without direct GitHub or Notion write access can still complete discovery and planning. It should produce:

- a validated bootstrap profile;
- a bootstrap plan;
- a private-core file tree and file contents;
- a Notion build checklist; and
- verification and rollback instructions.

The operator can then apply those artifacts manually or move the plan to another compatible host without repeating discovery.

## Read next

- [`BOOTSTRAP.md`](BOOTSTRAP.md) — executable conversational installer.
- [`docs/BOOTSTRAP_PROTOCOL.md`](docs/BOOTSTRAP_PROTOCOL.md) — architecture and state model.
- [`bootstrap/README.md`](bootstrap/README.md) — kit contents and extension points.
- [`docs/PRIVACY.md`](docs/PRIVACY.md) — privacy and trust boundaries.
