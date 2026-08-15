"""In-memory connector used by examples and tests."""

from __future__ import annotations

from dataclasses import dataclass, field

from peoples_grimoire.models import ProposedAction

from .base import ExecutionResult


@dataclass(slots=True)
class RecordingConnector:
    """Record actions without touching an external SaaS API."""

    name: str
    actions: list[ProposedAction] = field(default_factory=list)

    def execute(self, action: ProposedAction) -> ExecutionResult:
        self.actions.append(action)
        return ExecutionResult(
            external_id=action.target.external_id,
            url=action.target.url,
            detail={"recorded": True, "connector": self.name},
        )
