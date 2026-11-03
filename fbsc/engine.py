"""Deterministic nine-phase FBSC orchestration engine."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from .memory import SymbolicMemory
from .models import GhostLoop, Phase, PhaseRecord, SymbolicState
from .validation import DriftDetector

PhaseHandler = Callable[[str, SymbolicState], str]


@dataclass
class CycleResult:
    completed: bool
    output: str | None
    records: list[PhaseRecord] = field(default_factory=list)
    ghost_loop: GhostLoop | None = None
    message: str = ""


class FBSCEngine:
    """Runs phase handlers in strict order; failures are preserved, not hidden."""

    def __init__(self, memory: SymbolicMemory | None = None) -> None:
        self.state = SymbolicState()
        self.memory = memory
        if memory:
            self.state.identity = memory.get_identity()
            self.state.ghost_loops = memory.open_ghost_loops()

    def set_identity(self, key: str, value: object) -> None:
        self.state.identity[key] = value
        if self.memory:
            self.memory.set_identity(key, value)

    def run_cycle(self, text: str, handlers: dict[Phase, PhaseHandler] | None = None) -> CycleResult:
        if not text.strip():
            raise ValueError("Input cannot be empty.")
        handlers = handlers or {}
        current = text
        records: list[PhaseRecord] = []

        for phase in Phase:
            previous = records[-1].phase if records else None
            transition = DriftDetector.validate_transition(previous, phase)
            if not transition.valid:
                return self._suspend(text, phase, transition.reason, records)

            try:
                handler = handlers.get(phase, lambda value, _state: value)
                produced = handler(current, self.state)
                if not isinstance(produced, str) or not produced.strip():
                    raise ValueError("Phase handler returned an empty or non-text result.")
            except Exception as exc:
                return self._suspend(text, phase, f"Phase handler failed: {exc}", records)

            record = PhaseRecord(phase, current, produced)
            records.append(record)
            self.state.history.append(record)
            current = produced

        validation = DriftDetector.validate_cycle([record.phase for record in records])
        if not validation.valid:
            return self._suspend(text, Phase.RECURSION, validation.reason, records)

        self.state.cycle_count += 1
        self.state.last_output = current
        return CycleResult(True, current, records, message="Nine-phase cycle completed.")

    def _suspend(
        self, original: str, phase: Phase, reason: str, records: list[PhaseRecord]
    ) -> CycleResult:
        loop = GhostLoop(
            original_input=original,
            failed_phase=phase,
            reason=reason,
            unresolved_material={"completed_phases": [int(r.phase) for r in records]},
        )
        self.state.ghost_loops.append(loop)
        if self.memory:
            self.memory.store_ghost_loop(loop)
        return CycleResult(False, None, records, loop, reason)
