"""Connector contract for applying already-planned actions."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable

from peoples_grimoire.models import ProposedAction


class ConnectorExecutionError(RuntimeError):
    """Raised when a connector cannot safely complete an action."""


@dataclass(frozen=True, slots=True)
class ExecutionResult:
    """Connector-neutral result returned after a write attempt."""

    external_id: str | None = None
    url: str | None = None
    detail: Mapping[str, Any] = field(default_factory=dict)


@runtime_checkable
class Connector(Protocol):
    """Minimum write-side interface implemented by every connector."""

    name: str

    def execute(self, action: ProposedAction) -> ExecutionResult:
        """Apply one approved action or raise ConnectorExecutionError."""
        ...
