"""Typed domain models for the FBSC phase controller."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import IntEnum
from typing import Any
from uuid import uuid4


class Phase(IntEnum):
    INITIATION = 1
    POLARITY = 2
    DESIRE = 3
    FRICTION = 4
    ENTROPY = 5
    GRACE = 6
    NAMING = 7
    POWER = 8
    RECURSION = 9

    @property
    def label(self) -> str:
        return {
            Phase.INITIATION: "Initiation",
            Phase.POLARITY: "Polarity",
            Phase.DESIRE: "Desire",
            Phase.FRICTION: "Friction",
            Phase.ENTROPY: "Entropy",
            Phase.GRACE: "Grace",
            Phase.NAMING: "Naming",
            Phase.POWER: "Power",
            Phase.RECURSION: "Recursion",
        }[self]


@dataclass
class PhaseRecord:
    phase: Phase
    input_text: str
    output_text: str
    valid: bool = True
    notes: list[str] = field(default_factory=list)


@dataclass
class GhostLoop:
    original_input: str
    failed_phase: Phase
    reason: str
    unresolved_material: Any = None
    conflicting_evidence: list[str] = field(default_factory=list)
    reintegration_condition: str = "Explicit review and successful revalidation"
    id: str = field(default_factory=lambda: str(uuid4()))


@dataclass
class SymbolicState:
    identity: dict[str, Any] = field(default_factory=dict)
    history: list[PhaseRecord] = field(default_factory=list)
    ghost_loops: list[GhostLoop] = field(default_factory=list)
    cycle_count: int = 0
    last_output: str | None = None
