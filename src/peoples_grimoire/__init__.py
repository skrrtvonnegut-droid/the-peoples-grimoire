"""Reference runtime for The People's Grimoire."""

from .engine import GrimoireEngine, InMemoryLedger
from .models import (
    ActionRecord,
    ActionStatus,
    EventKind,
    GrimoireEvent,
    ProposedAction,
    ResourceRef,
)
from .validation import ValidationFailure, ValidationResult, validate_document, validate_path

__all__ = [
    "ActionRecord",
    "ActionStatus",
    "EventKind",
    "GrimoireEngine",
    "GrimoireEvent",
    "InMemoryLedger",
    "ProposedAction",
    "ResourceRef",
    "ValidationFailure",
    "ValidationResult",
    "validate_document",
    "validate_path",
]

__version__ = "0.0.1"
