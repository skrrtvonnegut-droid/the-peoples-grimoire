# Safe Observability

The runtime must be diagnosable without turning logs into a second copy of the applications it connects.

## Structured record envelope

`StructuredLogger` emits one JSON object per event. Every record contains the same correlation fields:

```json
{
  "timestamp": "2026-08-15T00:00:00+00:00",
  "level": "info",
  "event": "action.recorded",
  "correlation_id": "corr_opaque",
  "connector_id": "notion",
  "event_id": "evt_opaque",
  "action_id": "act_opaque",
  "recipe_id": "rcp_opaque",
  "debug": false,
  "fields": {
    "status": "awaiting_approval",
    "operation": "update",
    "resource_type": "page",
    "requires_approval": true
  }
}
```

Identifiers in this envelope are runtime-generated or intentionally opaque. Raw provider identifiers, titles, URLs, bodies, names, and email addresses do not belong in the envelope.

## Redaction order

Redaction is applied **before** JSON serialization and before a connector result enters operational detail.

1. Core secret field names—authorization, cookies, tokens, client secrets, private keys, passwords, API keys, and webhook secrets—become `[REDACTED]`.
2. Secret-shaped strings—including bearer credentials, JWTs, GitHub- and Notion-shaped tokens, PEM private keys, and generic secret assignments—become `[REDACTED]` regardless of field name.
3. Private identifiers and content fields become keyed fingerprints by default.
4. Connector manifests and recipes may add sensitive field names. They can only make handling stricter; they cannot exempt core secret fields.
5. Unknown connector payload fields are denied by default. The serializer returns an omitted-field count and a keyed payload fingerprint rather than the values.
6. Prompt-injection-shaped text is treated as untrusted data and replaced with an opaque marker when it reaches an otherwise safe scalar field.

Debug mode adds a `debug` marker. It does not expose a bypass switch.

## Keyed fingerprints

Fingerprints use HMAC-SHA-256 with an instance-specific key and a shortened opaque identifier such as `fp_12ab…`.

The key must come from a secret manager, operating-system keychain, or protected environment. It must not be committed. A keyed fingerprint is preferred to a plain hash because titles, email addresses, and common URLs may be guessable from a small dictionary.

Rotating the fingerprint key intentionally breaks correlation with historical fingerprints. That is useful when an operator wants old diagnostic material to become unlinkable.

## Connector result handling

`ExecutionResult` declares `safe_detail_fields`. Only those fields may appear as values in the operational result summary. Manifest- or recipe-sensitive fields are fingerprinted even when a connector mistakenly lists them as safe. Every other field is omitted.

External IDs and URLs returned after execution are represented by fingerprints in action detail. Connectors may retain the raw value only in an explicitly protected state component designed for identity linking.

## Exceptions

Exception messages are never copied into action detail or structured logs. The runtime records:

- a stable error code;
- the exception type;
- the correlation identifier already present in the log envelope; and
- a keyed diagnostic identifier derived from the correlation, type, and hidden message.

This lets a local operator connect repeated failures without exposing the message itself.

## Retention and deletion

The reference logger has **no internal persistence**. It writes a serialized record to the configured sink; the sink owns retention.

A deployment must define:

- where records are stored;
- the shortest useful retention window;
- who can read them;
- how records are deleted by time range or correlation identifier;
- whether backups inherit the same deletion schedule; and
- how fingerprint-key rotation affects historical correlation.

Deleting a runtime ledger does not automatically delete records copied into an external logging service. Deletion must be applied at every configured sink and backup location.

For local development, stdout with no durable capture is the safest default. Production deployments should use a dedicated restricted sink rather than general application logs.

## Test expectations

Connector and recipe tests should verify:

- core secret fields and secret-shaped values never appear in serialized output;
- private content becomes an opaque fingerprint;
- unknown payloads remain denied;
- debug mode preserves redaction;
- exception summaries reveal no message content;
- prompt-injection-shaped fixtures remain inert data; and
- declared safe fields contain only operational metadata.
