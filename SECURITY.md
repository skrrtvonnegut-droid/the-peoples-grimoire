# Security Policy

## Project status

The People’s Grimoire is pre-alpha and must not be trusted with production credentials or irreversible automation.

Only the current `main` branch receives security fixes during this stage.

## Report a vulnerability privately

Do not open a public issue for a suspected vulnerability, leaked credential, private payload, or privacy incident.

Use GitHub’s private vulnerability reporting or security-advisory feature for this repository. Include only the minimum information needed to reproduce the problem.

Before submitting:

- revoke or rotate any credential that may have been exposed;
- remove real personal content;
- replace account, repository, workspace, page, and tenant identifiers with synthetic values; and
- state whether the issue has been observed in a production account.

## Useful report contents

- affected component and version or commit;
- preconditions;
- reproduction steps using synthetic data;
- expected and observed behavior;
- potential confidentiality, integrity, or availability impact;
- whether a write, deletion, or cross-boundary disclosure occurred; and
- suggested mitigation, when known.

## Scope

Security concerns include:

- secret exposure;
- excessive connector permissions;
- authentication or authorization bypass;
- webhook signature failures;
- replay or duplicate execution;
- unsafe deserialization;
- command, prompt, path, or template injection;
- content treated as privileged instruction;
- cross-instance data leakage;
- unredacted logging;
- supply-chain compromise;
- silent destructive synchronization; and
- approval bypass.

## Secret handling

The project will not request production tokens in an issue, pull request, chat, email, fixture, or diagnostic bundle.

Credentials must be stored outside Git, including private repositories.

`.env.example` documents variable names only. A populated `.env` file is ignored and must remain local.

## Disclosure process

The maintainer of record will validate the report, coordinate a fix, and publish an advisory when disclosure is safe. Because the project is volunteer-maintained and pre-alpha, no response-time guarantee is offered.

Reporters will be credited when requested and when doing so does not increase risk.

## Safe harbor

Good-faith research intended to improve the project is welcome when it:

- avoids accessing data that does not belong to the researcher;
- avoids service disruption;
- uses synthetic accounts and fixtures;
- stops when sensitive data is encountered;
- reports privately; and
- allows a reasonable remediation period before disclosure.

This policy does not authorize testing against third-party SaaS platforms outside their own terms and security programs.
