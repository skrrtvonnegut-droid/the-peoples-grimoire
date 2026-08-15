"""Structured, content-minimizing observability primitives."""

from __future__ import annotations

import json
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from .redaction import DEFAULT_SAFE_LOG_FIELDS, Redactor


def new_correlation_id() -> str:
    return f"corr_{uuid4().hex}"


@dataclass(frozen=True, slots=True)
class LogContext:
    """Opaque identifiers needed to trace one event through the runtime."""

    correlation_id: str
    connector_id: str
    event_id: str | None = None
    action_id: str | None = None
    recipe_id: str | None = None

    def __post_init__(self) -> None:
        if not self.correlation_id.strip():
            raise ValueError("correlation_id must be non-empty")
        if not self.connector_id.strip():
            raise ValueError("connector_id must be non-empty")


@dataclass(slots=True)
class StructuredLogger:
    """Emit JSON records that never contain raw connector payloads by default."""

    sink: Callable[[str], None] = field(default=print, repr=False)
    redactor: Redactor = field(default_factory=Redactor)
    debug: bool = False

    def build_record(
        self,
        *,
        level: str,
        event: str,
        context: LogContext,
        fields: Mapping[str, Any] | None = None,
        sensitive_fields: Iterable[str] = (),
    ) -> dict[str, Any]:
        level_value = level.casefold()
        if level_value not in {"debug", "info", "warning", "error", "critical"}:
            raise ValueError(f"unsupported log level: {level!r}")

        safe_event = self.redactor.sanitize_scalar(event)
        return {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": level_value,
            "event": safe_event,
            "correlation_id": context.correlation_id,
            "connector_id": context.connector_id,
            "event_id": context.event_id,
            "action_id": context.action_id,
            "recipe_id": context.recipe_id,
            "debug": self.debug,
            "fields": self.redactor.sanitize_log_fields(
                fields,
                allowed_fields=DEFAULT_SAFE_LOG_FIELDS,
                sensitive_fields=sensitive_fields,
            ),
        }

    def emit(
        self,
        *,
        level: str,
        event: str,
        context: LogContext,
        fields: Mapping[str, Any] | None = None,
        sensitive_fields: Iterable[str] = (),
    ) -> dict[str, Any]:
        record = self.build_record(
            level=level,
            event=event,
            context=context,
            fields=fields,
            sensitive_fields=sensitive_fields,
        )
        self.sink(json.dumps(record, sort_keys=True, separators=(",", ":")))
        return record
