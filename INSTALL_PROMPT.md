# One-Prompt Installer

The easiest way to install **The People’s Grimoire** is to connect GitHub and Notion to a capable chatbot, then give the chatbot one bootstrap prompt.

The prompt is intentionally small. It does **not** duplicate the installer protocol. It tells the chatbot how to locate the public repository and hand control to the canonical [`BOOTSTRAP.md`](BOOTSTRAP.md), so improvements to the bootstrap protocol do not require people to keep copying a newer giant prompt.

## Before you run it

Through your chatbot host’s official integrations or connectors:

1. connect **GitHub**;
2. connect **Notion**; and
3. start a new conversation with the chatbot you want to use as your Grimoire’s cognition interface.

Use the narrowest permissions that still allow the installation you want. Never paste access tokens, cookies, client secrets, private keys, recovery codes, or other credentials into the conversation.

## Copy and paste this prompt

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

That is the installer.

The chatbot should now take over the installation as a guided conversation. You should not need to clone the public repository, download a ZIP, paste `BOOTSTRAP.md`, or manually construct the Grimoire unless your chatbot cannot read the public repository.

## What should happen next

A conforming chatbot will:

1. verify that it can actually read the public repository and your connected GitHub and Notion carriers;
2. ask for a bounded discovery scope;
3. inspect only the sources you approve;
4. infer a small durable topology from recurring patterns in your real work and knowledge;
5. search for existing canonical structures before proposing new ones;
6. show you the proposed GitHub and Notion changes before any durable write;
7. apply only the plan you approve; and
8. verify that a fresh capable AI could recover the instance from durable sources without depending on the original conversation.

## Why the installer works this way

The bootstrap prompt is an **ignition key**, not a second copy of the operating system.

The public repository remains authoritative for installation behavior, schemas, privacy boundaries, carrier roles, and continuity requirements. That gives the project one canonical bootstrap protocol while keeping onboarding simple enough to be: **connect two services, paste one prompt, review the plan**.

## Fallback when the chatbot cannot read the repository

If the chatbot cannot access the public GitHub repository, provide it with [`BOOTSTRAP.md`](BOOTSTRAP.md) and the supporting `bootstrap/`, `schemas/`, and `examples/bootstrap/` directories. The same protocol can then run in hybrid or portable-plan mode.
