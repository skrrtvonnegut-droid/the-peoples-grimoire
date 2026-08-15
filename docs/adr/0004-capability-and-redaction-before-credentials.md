# ADR 0004: Capability and redaction boundaries precede credentials

- **Status:** Accepted
- **Date:** 2026-08-15

## Context

A connector can expose more provider authority than one recipe needs. Credentials and logs can also reveal substantially more than the runtime requires to coordinate an action.

Treating capability descriptions and redaction as optional documentation would leave the core unable to distinguish intended authority from accidental implementation detail.

## Decision

Before a connector receives credentials or executes an action:

1. It must provide a machine-readable capability manifest.
2. The manifest must declare exact actions, resource types, required permissions, safety properties, sensitive fields, and protocol compatibility.
3. The runtime must refuse actions or recipe permissions absent from the declaration.
4. The active credential must satisfy the declared minimum scope.
5. Connector payloads and exceptions pass through deny-by-default redaction before diagnostic serialization.
6. Debug behavior cannot disable core secret filtering.
7. Connector conformance uses synthetic fixtures and transports rather than personal accounts.

## Consequences

- Connectors require more up-front design and test work.
- Broad provider SDK methods cannot be invoked merely because they are available.
- Recipes cannot widen credential or connector authority.
- Operators can inspect capability and risk before authorization.
- Logs remain useful for flow and status while omitting content.
- Some troubleshooting requires local correlation through opaque diagnostic identifiers instead of raw exception messages.

This constraint intentionally slows the acquisition of power so that trust grows first.
