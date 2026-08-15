"""Small internal value objects used by the execution engine."""

from __future__ import annotations

from dataclasses import dataclass

from .connectors.capabilities import CapabilityDecision


@dataclass(frozen=True, slots=True)
class ConnectorDecisionContext:
    operation: str | None = None
    requires_approval: bool = False
    irreversible: bool = False

    @classmethod
    def from_decision(cls, decision: CapabilityDecision) -> "ConnectorDecisionContext":
        return cls(
            operation=(
                decision.capability.operation.value
                if decision.capability is not None
                else None
            ),
            requires_approval=decision.requires_approval,
            irreversible=decision.irreversible,
        )
