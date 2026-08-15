"""Deny-by-default redaction for logs and connector diagnostics."""

from __future__ import annotations

import hmac
import json
import re
import secrets
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from hashlib import sha256
from typing import Any

REDACTED = "[REDACTED]"

_CORE_PROTECTED_FIELDS = frozenset(
    {
        "authorization",
        "proxyauthorization",
        "cookie",
        "setcookie",
        "accesstoken",
        "refreshtoken",
        "clientsecret",
        "privatekey",
        "webhooksecret",
        "password",
        "passwd",
        "apikey",
        "xapikey",
        "sessiontoken",
    }
)

_PRIVATE_FIELDS = frozenset(
    {
        "title",
        "name",
        "displayname",
        "email",
        "url",
        "externalid",
        "body",
        "content",
        "text",
        "description",
        "richtext",
        "pagetitle",
        "username",
    }
)

DEFAULT_SAFE_LOG_FIELDS = frozenset(
    {
        "status",
        "dry_run",
        "operation",
        "resource_type",
        "duration_ms",
        "error_code",
        "error_type",
        "diagnostic_id",
        "retryable",
        "missing_permissions",
        "undeclared_permissions",
        "requires_approval",
        "irreversible",
        "recorded",
        "connector",
        "count",
        "attempt",
        "http_status",
        "result",
    }
)

_SECRET_PATTERNS = (
    re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=-]{12,}", re.IGNORECASE),
    re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\b"),
    re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,})\b"),
    re.compile(r"\b(?:secret|ntn)_[A-Za-z0-9_-]{20,}\b"),
    re.compile(
        r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----.*?"
        r"-----END (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
        re.DOTALL,
    ),
    re.compile(
        r"(?i)\b(?:access[_-]?token|refresh[_-]?token|client[_-]?secret|"
        r"api[_-]?key|password|webhook[_-]?secret)\b\s*[:=]\s*[^\s,;]{8,}"
    ),
)

_PROMPT_INJECTION_PATTERN = re.compile(
    r"(?i)(?:ignore|disregard|override|forget).{0,60}"
    r"(?:previous|system|developer).{0,30}instructions?|"
    r"(?:reveal|print|return).{0,40}(?:system prompt|hidden instructions)"
)


def _normalize_field_name(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.casefold())


def _contains_secret(value: str) -> bool:
    return any(pattern.search(value) for pattern in _SECRET_PATTERNS)


def _contains_prompt_injection(value: str) -> bool:
    return bool(_PROMPT_INJECTION_PATTERN.search(value))


@dataclass(slots=True)
class Redactor:
    """Keyed fingerprints plus non-bypassable secret filtering."""

    fingerprint_key: bytes = field(
        default_factory=lambda: secrets.token_bytes(32),
        repr=False,
    )

    def __post_init__(self) -> None:
        if len(self.fingerprint_key) < 16:
            raise ValueError("fingerprint_key must contain at least 16 bytes")

    def fingerprint(self, value: Any) -> str:
        canonical = json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            default=str,
        ).encode()
        digest = hmac.new(self.fingerprint_key, canonical, sha256).hexdigest()[:20]
        return f"fp_{digest}"

    def sanitize_scalar(self, value: Any, *, private: bool = False) -> Any:
        if value is None or isinstance(value, bool | int | float):
            return value
        if isinstance(value, bytes):
            return REDACTED
        if isinstance(value, str):
            if _contains_secret(value):
                return REDACTED
            if private:
                return self.fingerprint(value)
            if _contains_prompt_injection(value):
                return f"[UNTRUSTED_TEXT:{self.fingerprint(value)}]"
            if len(value) > 256:
                return self.fingerprint(value)
            return value
        if isinstance(value, Mapping):
            return {"fingerprint": self.fingerprint(value), "type": "mapping"}
        if isinstance(value, Sequence):
            return [self.sanitize_scalar(item) for item in list(value)[:20]]
        return self.fingerprint(value)

    def sanitize_log_fields(
        self,
        fields: Mapping[str, Any] | None,
        *,
        allowed_fields: Iterable[str] = DEFAULT_SAFE_LOG_FIELDS,
        sensitive_fields: Iterable[str] = (),
    ) -> dict[str, Any]:
        """Serialize only known operational fields; summarize everything else."""

        if not fields:
            return {}

        allowed = {_normalize_field_name(field) for field in allowed_fields}
        additional_sensitive = {
            _normalize_field_name(field) for field in sensitive_fields
        }
        sanitized: dict[str, Any] = {}
        omitted = 0

        for key, value in fields.items():
            normalized = _normalize_field_name(str(key))
            safe_key = re.sub(r"[^a-zA-Z0-9_]", "_", str(key)).strip("_").casefold()
            safe_key = safe_key or "field"

            if normalized in _CORE_PROTECTED_FIELDS:
                sanitized[safe_key] = REDACTED
            elif normalized in additional_sensitive:
                sanitized[f"{safe_key}_fingerprint"] = self.fingerprint(value)
            elif normalized in _PRIVATE_FIELDS:
                sanitized[f"{safe_key}_fingerprint"] = self.fingerprint(value)
            elif normalized in allowed:
                sanitized[safe_key] = self.sanitize_scalar(value)
            else:
                omitted += 1

        if omitted:
            sanitized["omitted_field_count"] = omitted
            sanitized["omitted_fields_fingerprint"] = self.fingerprint(fields)
        return sanitized

    def sanitize_connector_payload(
        self,
        payload: Mapping[str, Any] | None,
        *,
        safe_fields: Iterable[str] = (),
        sensitive_fields: Iterable[str] = (),
    ) -> dict[str, Any]:
        """Deny unknown payload fields and return only an operational summary."""

        if not payload:
            return {
                "fields": {},
                "omitted_field_count": 0,
                "payload_fingerprint": self.fingerprint({}),
            }

        safe = {_normalize_field_name(field) for field in safe_fields}
        sensitive = {_normalize_field_name(field) for field in sensitive_fields}
        fields: dict[str, Any] = {}
        omitted = 0

        for key, value in payload.items():
            normalized = _normalize_field_name(str(key))
            safe_key = re.sub(r"[^a-zA-Z0-9_]", "_", str(key)).strip("_").casefold()
            safe_key = safe_key or "field"

            if normalized in _CORE_PROTECTED_FIELDS:
                fields[safe_key] = REDACTED
            elif normalized in sensitive or normalized in _PRIVATE_FIELDS:
                fields[f"{safe_key}_fingerprint"] = self.fingerprint(value)
            elif normalized in safe:
                fields[safe_key] = self.sanitize_scalar(value)
            else:
                omitted += 1

        return {
            "fields": fields,
            "omitted_field_count": omitted,
            "payload_fingerprint": self.fingerprint(payload),
        }

    def private_fingerprint(self, value: Any) -> str:
        return self.fingerprint(value)


def safe_exception_summary(
    exc: BaseException,
    *,
    correlation_id: str,
    redactor: Redactor,
) -> dict[str, str]:
    """Return a diagnostic handle without serializing the exception message."""

    error_type = type(exc).__name__
    diagnostic_id = "diag_" + redactor.fingerprint(
        {
            "correlation_id": correlation_id,
            "error_type": error_type,
            "message": str(exc),
        }
    ).removeprefix("fp_")
    return {
        "error_code": "operation_failed",
        "error_type": error_type,
        "diagnostic_id": diagnostic_id,
    }
